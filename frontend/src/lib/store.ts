import type {FarmData} from './types'
const KEY='agrios-v01'
const initial:FarmData={farmer:'Usman',farm:'Green Valley Farm',city:'Karachi',crops:[{id:'sample-rice',name:'Rice',plantingDate:'2026-08-10',harvestDate:'2026-12-10',area:4,sample:true},{id:'sample-wheat',name:'Wheat',plantingDate:'2026-11-01',harvestDate:'2027-03-15',area:3,sample:true}],soil:[{id:'sample-soil',date:new Date().toISOString().slice(0,10),ph:6.8,moisture:31,nitrogen:42,phosphorus:28,potassium:35,sample:true}]}
export function loadData():FarmData{try{return JSON.parse(localStorage.getItem(KEY)||'null')||initial}catch{return initial}}
export function saveData(data:FarmData){localStorage.setItem(KEY,JSON.stringify(data))}
