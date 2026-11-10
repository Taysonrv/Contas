"""Leitura local do XLSX com a biblioteca padrão. Não altera a planilha."""
import argparse, json, zipfile, datetime
from pathlib import Path
import xml.etree.ElementTree as ET

NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def load(source, year=2026):
    with zipfile.ZipFile(source) as z:
        strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)] if 'xl/sharedStrings.xml' in z.namelist() else []
        def sheet(name):
            result={}
            for c in ET.fromstring(z.read(name)).findall('.//m:c',NS):
                v=c.find('m:v',NS)
                if c.get('t')=='inlineStr': value=''.join(c.find('m:is',NS).itertext())
                elif v is None: continue
                elif c.get('t')=='s': value=strings[int(v.text)]
                else:
                    try: value=float(v.text)
                    except (ValueError,TypeError): value=v.text
                result[c.get('r')]=value
            return result
        cells=sheet('xl/worksheets/sheet1.xml'); records=[]; months=set()
        for owner,start,end,header in [('Tayson',3,11,2),('Ellissyanne',19,25,18)]:
            for col,month in [('B',10),('C',11),('D',12),('E',1),('F',2)]:
                if not cells.get(f'{col}{header}'): continue
                key=f'{year if month>=10 else year+1}-{month:02}'
                months.add(key)
                for row in range(start,end+1):
                    value=cells.get(f'{col}{row}'); label=str(cells.get(f'A{row}','')).strip()
                    if value is None or not label: continue
                    paid=isinstance(value,str) and value.strip().upper()=='PAGO'
                    amount=round(value,2) if isinstance(value,(int,float)) else None
                    if not paid and amount is None: continue
                    records.append(dict(id=f'{col}{row}',month=key,owner=owner,name=label,amount=amount,paid=paid,day=None,source=f'CONTAS MENSAIS!{col}{row}'))
        trips=[]; travel=sheet('xl/worksheets/sheet2.xml')
        for namecol,datecol,valcol,statuscol,start,title in [('A','B','C','D',3,1),('F','G','H','I',3,1),('K','L','M','N',3,1),('A','B','C','D',20,18),('F','G','H','I',20,18),('K','L','M','N',20,18),('P','Q','R','S',20,18)]:
            for row in range(start,start+12):
                serial=travel.get(f'{datecol}{row}')
                if not isinstance(serial,(int,float)): continue
                date=(datetime.datetime(1899,12,30)+datetime.timedelta(days=serial)).date().isoformat()
                trips.append(dict(id=f'trip-{valcol}{row}',owner=travel.get(f'{namecol}{title}'),date=date,amount=travel.get(f'{valcol}{row}'),paid=travel.get(f'{statuscol}{row}')=='PAGO',installment=travel.get(f'{namecol}{row}')))
        return dict(months=sorted(months),records=records,trips=trips,importedAt=datetime.datetime.now().isoformat(),source=Path(source).name,notes=['Ano-base assumido: outubro a dezembro de '+str(year)+'; janeiro e fevereiro de '+str(year+1)+'.','PAGO sem valor é preservado como valor desconhecido. Zeros da origem são preservados.','Resumos calculados pelas linhas; totais em cache da planilha não são usados.','As parcelas da viagem são exibidas separadamente para evitar somá-las novamente à conta VIAGEM NATAL.'])

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('file'); parser.add_argument('--year',type=int,default=2026); args=parser.parse_args()
    output=Path(__file__).resolve().parents[1]/'data'/'accounts.json'; output.parent.mkdir(exist_ok=True)
    data=load(args.file,args.year); output.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Importados {len(data["records"])} lançamentos e {len(data["trips"])} parcelas em {output}')
