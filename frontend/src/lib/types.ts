export type Crop = {id:string;name:string;plantingDate:string;harvestDate:string;area:number;sample?:boolean}
export type SoilTest = {id:string;date:string;ph:number;moisture:number;nitrogen:number;phosphorus:number;potassium:number;sample?:boolean}
export type FarmData = {farmer:string;farm:string;city:string;crops:Crop[];soil:SoilTest[]}
