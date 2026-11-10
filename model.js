export const sum=items=>Math.round(items.reduce((n,r)=>n+(typeof r.amount==='number'?r.amount:0),0)*100)/100;
export function summary(records,income){const total=sum(records),pending=sum(records.filter(r=>!r.paid));return {total,pending,balance:income-total,unknown:records.filter(r=>r.amount===null).length,paid:records.filter(r=>r.paid).length};}
