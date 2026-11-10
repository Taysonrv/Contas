import test from 'node:test';
import assert from 'node:assert/strict';
import {sum,summary} from './model.js';
test('valores desconhecidos não viram pagamentos de valor zero',()=>{const rows=[{amount:null,paid:true},{amount:120,paid:false},{amount:54.9,paid:true}];assert.deepEqual(summary(rows,1000),{total:174.9,pending:120,balance:825.1,unknown:1,paid:2});});
test('soma monetária arredonda centavos e mantém zero informado',()=>assert.equal(sum([{amount:0},{amount:0.1},{amount:0.2}]),0.3));
