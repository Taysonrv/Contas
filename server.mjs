import http from 'node:http';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
const root=process.cwd(), port=Number(process.env.PORT||5173);
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.json':'application/json'};
http.createServer(async(req,res)=>{
 const url=new URL(req.url,'http://localhost');
 const pathname=url.pathname==='/'?'/index.html':decodeURIComponent(url.pathname);
 if(!['/index.html','/app.js','/styles.css','/model.js','/data/accounts.json'].includes(pathname)){res.writeHead(404);res.end('Não encontrado');return;}
 try{const body=await readFile(path.join(root,pathname));res.writeHead(200,{'Content-Type':types[path.extname(pathname)],'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(body);}catch{res.writeHead(404);res.end('Arquivo não encontrado. Execute a importação da planilha.');}
}).listen(port,'127.0.0.1',()=>console.log(`Contas: http://localhost:${port}`));
