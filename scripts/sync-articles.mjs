import {ARTICLES} from '../docs/lab/articles.mjs';
import {readFileSync, writeFileSync, existsSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

function md(a){
const d=a.definitions.map(([t,v])=>`| ${t} | ${v} |`).join("\n");
const src=a.sources.map(([label,url])=>`- [${label}](${url})`).join("\n");
return `# ${a.id} — ${a.title}\n\n**Status científico:** ${a.status}  \n**Tipo:** ${a.kind}\n\n> ${a.question}\n\n## Intuição\n\n${a.intuition}\n\n## Motivação\n\n${a.motivation}\n\n## Definições mínimas\n\n| Conceito | Significado |\n|---|---|\n${d}\n\n## Formulação\n\n\`\`\`text\n${a.formula}\n\`\`\`\n\n## Exemplo\n\n${a.example}\n\n## Resultado / hipótese\n\n${a.finding}\n\n## Por que importa para o CDKA?\n\n${a.bigger}\n\n## O que habilita em seguida?\n\n${a.next}\n\n## Limites e possíveis falsificações\n\n${a.limits}\n\n## Simulador e visualização\n\n${a.simulator}\n\n[Abrir laboratório interativo](../index.html#${a.id.toLowerCase()}) (quando hospedado como site estático).\n\n## Referências e proveniência\n\n${src}\n\n---\n\n*CDKA · Texto de pesquisa sujeito a revisão. Não atribuir originalidade aos resultados identificados como conhecidos.*\n`;
}

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const check=process.argv.includes('--check');
let mismatches=0;
for(const article of ARTICLES){
  const path=resolve(root,'docs/articles/'+article.id+'.md');
  const expected=md(article);
  if(check){
    if(!existsSync(path)||readFileSync(path,'utf8')!==expected){
      console.error('Article is not synchronized: '+article.id);
      mismatches++;
    }
  }else{
    writeFileSync(path,expected,'utf8');
    console.log('Generated '+article.id);
  }
}
if(check){
  if(mismatches){
    console.error(mismatches+' articles are out of sync. Run: npm run articles:write');
    process.exitCode=1;
  }else console.log(ARTICLES.length+' canonical articles are synchronized.');
}
