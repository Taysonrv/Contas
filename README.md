# Contas

App local de finanças familiares inspirado na referência fornecida. JavaScript e CSS, sem dependências de instalação. Requer Node.js 20+ e Python 3 para importar o Excel.

## Testar no VS Code (PowerShell)

```powershell
cd "C:\Users\Tayson\Documents\ChatGPT\Contas"
code .
python scripts/import_sheet.py "D:\Tayson\PLANILHA DE CONTAS - ATUALIZADA 2026.xlsx"
npm test
npm run dev
```

Abra http://localhost:5173. Encerre o servidor com Ctrl+C. Não é necessário executar npm install.

## Uso

- Navegue pelos meses nas setas ou no seletor.
- Cadastre a renda conjunta em Nossa renda para calcular o saldo previsto.
- Marque contas como pagas e adicione lançamentos pelo botão Adicionar conta.
- Use Fluxo de caixa para buscar e consultar todas as contas do mês.
- Consulte as parcelas e pagamentos individuais em Viagem Natal.
- Execute novamente o comando de importação e atualize o navegador quando o Excel mudar.

## Dados e critérios

O importador lê as duas abas do formato fornecido usando a biblioteca padrão do Python, sem abrir ou modificar o Excel. Não executa macros nem instruções encontradas no arquivo. Os meses outubro–dezembro são associados a 2026 e janeiro–fevereiro a 2027, uma suposição porque os cabeçalhos não têm ano. Ajuste o ano-base usando `--year 2026`.

Os totais são calculados a partir dos lançamentos individuais; os totais em cache do Excel podem estar desatualizados. Células PAGO sem valor são exibidas como valor não informado e não entram na soma. Zeros são mantidos; células vazias não criam contas. Não há vencimentos para as contas mensais na origem. A viagem fica separada, pois existe também uma linha VIAGEM NATAL nas contas mensais, evitando duplicidade.

O arquivo `data/accounts.json` contém os dados financeiros e é ignorado pelo Git, assim como arquivos Excel. Cada computador precisa importar sua própria planilha. Pagamentos, renda e novas contas ficam no localStorage deste navegador, separados por mês. Esses registros não sincronizam entre dispositivos nem são escritos de volta na planilha. Uma marcação manual de pagamento prevalece sobre a importação para a mesma célula e mês. Limpar os dados do navegador remove as alterações locais. O servidor escuta apenas no computador local.

O layout utiliza a fonte DM Sans quando houver internet, com Arial como alternativa. Não há serviços financeiros ou dados fictícios no app.
