import {useEffect,useState} from 'react'
import type {ReactNode} from 'react'
import {NavLink,Routes,Route,useNavigate} from 'react-router-dom'
import {Sprout,LayoutDashboard,Leaf,Droplets,ScanSearch,CloudSun,Settings as SettingsIcon,Activity,Plus,Trash2,Languages,Cloud,Wind,Sun} from 'lucide-react'
import {useTranslation} from 'react-i18next'
import i18n from './i18n'
import {loadData,saveData} from './lib/store'
import {cropNames,cropGuides} from './lib/crops'
import type {FarmData,Crop} from './lib/types'
import FieldMap from './components/FieldMap'
import {api} from './lib/api'
import {getWeather} from './lib/weather'

const nav=[['/','dashboard',LayoutDashboard],['/crops','crops',Leaf],['/soil','soil',Sprout],['/irrigation','irrigation',Droplets],['/detect','detect',ScanSearch],['/weather','weather',CloudSun],['/settings','settings',SettingsIcon]] as const
function Layout({children}:{children:ReactNode}){const {t}=useTranslation();return <div className="shell"><aside className="sidebar"><div className="logo"><Sprout size={23}/></div>{nav.map(([to,key,Icon])=><NavLink end to={to} key={to} title={t(key)} className={({isActive})=>'navbtn '+(isActive?'active':'')}><Icon size={20}/></NavLink>)}</aside><main className="content">{children}</main></div>}
function App(){const [data,setData]=useState<FarmData>(loadData);useEffect(()=>saveData(data),[data]);const update=(patch:Partial<FarmData>)=>setData(d=>({...d,...patch}));return <Layout><Routes><Route path="/" element={<Dashboard data={data}/>}/><Route path="/crops" element={<Crops data={data} update={update}/>}/><Route path="/soil" element={<Soil data={data} update={update}/>}/><Route path="/irrigation" element={<Irrigation data={data}/>}/><Route path="/detect" element={<Detect/>}/><Route path="/weather" element={<Weather city={data.city}/>}/><Route path="/settings" element={<Settings data={data} update={update}/>}/></Routes></Layout>}
function Header({title,subtitle}:{title:string;subtitle:string}){const {t}=useTranslation();return <header className="top"><div><h1 className="serif" style={{fontSize:34,margin:'0 0 5px'}}>{title}</h1><div className="muted">{subtitle}</div></div><div style={{display:'flex',gap:10,alignItems:'center'}}><select className="field" style={{width:110}} value={i18n.language} onChange={e=>{i18n.changeLanguage(e.target.value);localStorage.setItem('agrios-language',e.target.value);document.documentElement.dir=e.target.value==='en'?'ltr':'rtl'}}><option value="en">English</option><option value="ur">اردو</option><option value="sd">سنڌي</option></select><div className="secondary" style={{borderRadius:12}}> {title===' ' ? 'Farm' : 'GV'} · PK</div></div></header>}
function Dashboard({data}:{data:FarmData}){const {t}=useTranslation();const soil=data.soil[data.soil.length-1];return <><Header title={`Hi, ${data.farmer}!`} subtitle={t('subtitle')}/><div className="gridmain"><div className="stack"><section className="card weather"><div className="muted">{t('weatherCard')} · {data.city}</div><div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}><div><div className="serif" style={{fontSize:55}}>18</div><b>November 2026</b></div><Sun size={48} color="#d99a32"/></div><div className="metrics" style={{marginTop:18}}><div className="pill">Temperature <b>29°C</b></div><div className="pill">Wind <b>12 km/h</b></div><div className="pill">Humidity <b>68%</b></div></div><small className="muted">Illustrative sample card — connect live weather in Weather.</small></section><div className="statrow"><div className="card"><div className="muted">{t('plantHealth')}</div><div className="serif stat">95%</div><span className="green">Excellent · sample</span></div><div className="card"><div className="muted">{t('activeZones')}</div><div className="serif stat">{data.crops.length}</div><span className="green">Crop records</span></div></div><div className="card"><b>{t('soilStatus')}</b><p className="muted">Latest manual soil test · {soil?.date||'No record'}</p><div className="bar"><span style={{width:`${Math.min(100,soil?.moisture||0)}%`}}/></div><p className="green">{t('optimal')} · pH {soil?.ph??'—'}</p></div><div className="statrow"><div className="card"><b>Auto Watering</b><p className="muted">Planning toggle · not connected to hardware</p><input type="checkbox" aria-label="Auto watering planning toggle"/></div><div className="card"><b>Soil pH</b><div className="serif stat">{soil?.ph??'—'}</div><span className="muted">Manual entry</span></div></div><div className="card"><b>Fertilizer application guidance</b><div style={{height:12,borderRadius:10,marginTop:16,background:'linear-gradient(90deg,#d65a4a,#e9b34c,#4a9a68)'}}/><p className="muted">General guidance only — use a current soil test.</p></div></div><div className="stack"><div className="card"><div style={{display:'flex',justifyContent:'space-between',marginBottom:12}}><div><b>Field overview</b><p className="muted">Select a parcel to inspect the zone</p></div><span className="badge">Sample map</span></div><FieldMap/></div><div className="bottomgrid"><div className="card"><b>{t('growth')}</b><div className="serif" style={{fontSize:54,marginTop:20}}>87%</div><div className="bar"><span style={{width:'87%'}}/></div><p className="muted">Max 96 · Min 62 · Avg 81 · sample</p></div><div className="card"><b>{t('assistant')}</b><p className="muted">Ask about crops, soil, or farm planning.</p><Chat/></div></div><div className="card"><b>{t('quickActions')}</b><div className="actions" style={{marginTop:12}}><NavLink className="secondary" to="/crops">{t('addCrop')}</NavLink><NavLink className="secondary" to="/soil">{t('logSoil')}</NavLink><NavLink className="secondary" to="/detect">{t('detect')}</NavLink></div></div></div></div></>}
function Chat(){const [q,setQ]=useState('');const [answer,setAnswer]=useState('');return <form onSubmit={async e=>{e.preventDefault();try{const r=await api<any>('/assistant/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});setAnswer(r.answer)}catch{setAnswer('Backend unavailable. Start the FastAPI server to use the assistant.')}}}><input className="field" value={q} onChange={e=>setQ(e.target.value)} placeholder="Ask anything…"/><button className="primary" style={{marginTop:8}}>Send</button>{answer&&<p className="muted">{answer}</p>}</form>}
function Crops({data,update}:{data:FarmData;update:(p:Partial<FarmData>)=>void}){const {t}=useTranslation();const [name,setName]=useState('Rice'),[date,setDate]=useState('2026-11-18'),[area,setArea]=useState('1');function add(){const c:Crop={id:crypto.randomUUID(),name,plantingDate:date,harvestDate:'',area:Number(area)};update({crops:[...data.crops,c]})}return <><Header title={t('crops')} subtitle="Manage crop records and field tasks."/><div className="card"><h3>Add a crop</h3><div className="statrow"><select className="field" value={name} onChange={e=>setName(e.target.value)}>{cropNames.map(c=><option key={c}>{c}</option>)}</select><input className="field" type="date" value={date} onChange={e=>setDate(e.target.value)}/></div><input className="field" style={{marginTop:10}} type="number" min="0.01" step=".01" value={area} onChange={e=>setArea(e.target.value)} placeholder={t('area')}/><button className="primary" style={{marginTop:12}} onClick={add}><Plus size={16}/> {t('save')}</button></div><div className="stack" style={{marginTop:16}}>{data.crops.map(c=><div className="card" key={c.id} style={{display:'flex',justifyContent:'space-between',gap:10}}><div><b>{c.name}</b> {c.sample&&<span className="badge">Sample</span>}<p className="muted">Planted {c.plantingDate} · {c.area} acres</p><small>{cropGuides[c.name]}</small></div><button className="secondary" onClick={()=>update({crops:data.crops.filter(x=>x.id!==c.id)})}><Trash2 size={16}/></button></div>)}</div></>}
function Soil({data,update}:{data:FarmData;update:(p:Partial<FarmData>)=>void}){const [ph,setPh]=useState('7'),[moisture,setMoisture]=useState('30');return <><Header title="Soil & Nutrients" subtitle="Record manual soil tests. Values are not sensor readings."/><div className="card"><h3>New manual soil test</h3><div className="statrow"><label>pH<input className="field" type="number" step=".1" value={ph} onChange={e=>setPh(e.target.value)}/></label><label>Moisture %<input className="field" type="number" value={moisture} onChange={e=>setMoisture(e.target.value)}/></label></div><button className="primary" style={{marginTop:12}} onClick={()=>update({soil:[...data.soil,{id:crypto.randomUUID(),date:new Date().toISOString().slice(0,10),ph:Number(ph),moisture:Number(moisture),nitrogen:0,phosphorus:0,potassium:0}]})}>Save soil test</button></div>{data.soil.map(s=><div className="card" key={s.id} style={{marginTop:12}}> <b>{s.date}</b> {s.sample&&<span className="badge">Sample</span>}<p className="muted">pH {s.ph} · moisture {s.moisture}% · N {s.nitrogen} · P {s.phosphorus} · K {s.potassium}</p></div>)}</>}
function Irrigation({data}:{data:FarmData}){const [rain,setRain]=useState('0'),[temp,setTemp]=useState('30');const soil=data.soil[data.soil.length-1];const moisture=soil?.moisture;const status=moisture==null?'unknown':Number(rain)>=12&&moisture>=30?'skip':moisture<18||Number(temp)>=36?'urgent':moisture<28?'due':'ok';return <><Header title="Irrigation planning" subtitle="Rule-based estimate using manual moisture and entered weather values."/><div className="card"><p>Latest manual moisture: <b>{moisture??'Not recorded'}%</b></p><div className="statrow"><label>48h forecast rainfall (mm)<input className="field" value={rain} onChange={e=>setRain(e.target.value)} type="number"/></label><label>Temperature °C<input className="field" value={temp} onChange={e=>setTemp(e.target.value)} type="number"/></label></div><h2 className="serif" style={{textTransform:'uppercase'}}>{status}</h2><p className="muted">Estimate only. Verify soil and crop conditions in the field before irrigation.</p></div></>}
function Detect(){
  const [file,setFile]=useState<File|null>(null);
  const [preview,setPreview]=useState('');
  const [crop,setCrop]=useState('');
  const [modelInfo,setModelInfo]=useState<{supported_crops:string[],status:string,error?:string}|null>(null);
  useEffect(()=>{api<{supported_crops:string[],status:string,error?:string}>('/model/info').then(setModelInfo).catch(()=>setModelInfo(null))},[]);
  const [result,setResult]=useState<any>(null);
  const [busy,setBusy]=useState(false);
  const [error,setError]=useState('');

  useEffect(()=>{
    if(!file){setPreview('');return}
    const url=URL.createObjectURL(file);
    setPreview(url);
    return ()=>URL.revokeObjectURL(url);
  },[file]);

  function chooseFile(next:File|null){setFile(next);setResult(null);setError('')}

  async function run(){
    if(!file)return;
    if(!crop){setError('Please select the crop shown in the image before analysis.');return}
    setBusy(true);setError('');setResult(null);
    const fd=new FormData();
    fd.append('image',file);
    fd.append('crop_hint',crop);
    try{const r=await api<any>('/detect',{method:'POST',body:fd});setResult(r)}
    catch(e){setError(e instanceof Error?e.message:'Detection failed')}
    finally{setBusy(false)}
  }

  return <>
    <Header title="AI Disease Detection" subtitle="Upload a clear leaf image, select its crop, and review the model result."/>
    <div className="detect-layout">
      <section className="card detect-upload">
        <div className="detect-section-heading"><div><span className="detect-kicker">STEP 01</span><h2>Upload leaf image</h2><p className="muted">Use a clear, well-lit photo focused on one leaf.</p></div><span className="detect-icon">⌁</span></div>
        <label className="detect-field-label" htmlFor="detect-crop">Crop in the photograph</label>
        <select id="detect-crop" className="field detect-select" value={crop} onChange={e=>{setCrop(e.target.value);setResult(null);setError('')}}>
          <option value="">Select a crop</option>
          {(modelInfo?.supported_crops || ['Apple','Blueberry','Cherry','Corn','Grape','Orange','Peach','Pepper','Potato','Raspberry','Soybean','Squash','Strawberry','Tomato']).map(name=><option key={name} value={name}>{name}</option>)}
        </select>
        <p className="detect-hint">All 14 supported crops are listed. Selecting the crop checks whether the top prediction matches it.</p>
        <label className="detect-dropzone" htmlFor="detect-image">
          <span className="detect-upload-symbol">↑</span>
          <strong>{file?'Choose a different image':'Choose a leaf image'}</strong>
          <span className="muted">JPG, PNG or WebP · Maximum 8 MB</span>
          <input id="detect-image" type="file" accept="image/jpeg,image/png,image/webp" onChange={e=>chooseFile(e.target.files?.[0]||null)}/>
        </label>
        {preview&&<div className="detect-preview-wrap"><div className="detect-preview-heading"><strong>Image preview</strong><span className="muted">{file?.name}</span></div><img className="detect-preview" src={preview} alt="Selected crop leaf preview"/></div>}
        {error&&<div className="detect-error" role="alert">{error}</div>}
        <button className="primary detect-submit" disabled={!file||!crop||busy} onClick={run}>{busy?'Analyzing image…':'Analyze image'}</button>
        <p className="muted">Model: Daksh159 MobileNetV2 · Status: {modelInfo?.status||"backend unavailable"}{modelInfo?.error?` (${modelInfo.error})`:""}</p><p className="detect-disclaimer">AI output is an initial screening aid, not a confirmed agricultural diagnosis.</p>
      </section>

      <section className="card detect-result-panel">
        <span className="detect-kicker">STEP 02</span><h2>Analysis results</h2>
        {!result&&!busy&&<div className="detect-empty"><div className="detect-empty-icon">✳</div><strong>Your result will appear here</strong><p className="muted">Upload an image and select its crop to begin analysis.</p></div>}
        {busy&&<div className="detect-empty"><div className="detect-spinner"/><strong>Analyzing your image</strong><p className="muted">The AI model is processing the uploaded leaf.</p></div>}
        {result&&<div className="detect-result-content">
          {result.unsupported||result.type==='mismatch'?<div className="detect-warning-card"><span className="detect-status-pill">{result.unsupported?'Crop not supported':'Crop mismatch'}</span><h3>{result.crop}</h3><strong>{result.disease}</strong><p>{result.message}</p><div className="detect-next-step"><b>What this means</b><span>{result.unsupported?'The current model was not trained to diagnose this crop. No disease has been identified.':'The model returned a class for a different crop, so AgriOS has withheld the diagnosis.'}</span></div><p className="muted">{result.model_guess?`Nearest model class (not a diagnosis): ${result.model_guess}`:''}</p></div>:<>
            <div className="detect-result-heading"><div><span className="detect-field-label">Selected crop</span><h3>{result.crop}</h3></div><span className={result.uncertain?'detect-status-pill':'detect-status-pill detect-status-ok'}>{result.uncertain?'Needs verification':result.healthy?'Healthy class':'Disease class'}</span></div>
            <div className="detect-disease-card"><span className="detect-field-label">Model classification</span><h2>{result.disease}</h2><p>{result.uncertain?'This is an uncertain model prediction. Do not treat it as a confirmed diagnosis.':result.healthy?'The model selected a healthy-plant class. Continue routine field monitoring.':'The model selected this disease class. Confirm symptoms before taking action.'}</p><div className="detect-confidence-row"><span>Model score</span><strong>{(result.confidence*100).toFixed(1)}%</strong></div><div className="detect-confidence-track"><span style={{width:`${Math.max(0,Math.min(100,result.confidence*100))}%`}}/></div><small className="muted">Softmax score; it is not a calibrated probability of correctness.</small></div>
            {result.top?.length>0&&<div className="detect-top-classes"><h4>Other model classes</h4>{result.top.map((x:any)=><div className="detect-top-item" key={x.label}><div><span>{x.label}</span><b>{(x.score*100).toFixed(1)}%</b></div><div className="detect-confidence-track"><span style={{width:`${Math.max(0,Math.min(100,x.score*100))}%`}}/></div></div>)}</div>}
            {result.uncertain&&<div className="detect-warning-inline">Prediction uncertainty is elevated. Seek confirmation from a local agriculture specialist before applying treatment.</div>}
          </>}
        </div>}
      </section>
    </div>
    <div className="detect-model-note"><strong>Model limitation</strong><span>This model supports 14 crop types and 38 disease/healthy image classes. It does not diagnose wheat, rice, cotton, sugarcane, onion, or mango. Class-index order follows the standard PlantVillage alphabetical convention and should be verified against the original training code.</span></div>
  </>
}
function Weather({city}:{city:string}){const [w,setW]=useState<any>(null),[err,setErr]=useState('');useEffect(()=>{getWeather(city).then(setW).catch(e=>setErr(e.message))},[city]);return <><Header title="Weather" subtitle="Live forecast data from Open-Meteo."/><div className="card">{err&&<p>{err}</p>}{w&&<><h2 className="serif">{w.place}</h2><div className="serif" style={{fontSize:54}}>{w.current.temperature_2m}°C</div><p>Feels like {w.current.apparent_temperature}°C · Humidity {w.current.relative_humidity_2m}% · Wind {w.current.wind_speed_10m} km/h</p><p>48-hour rainfall probability aggregate (rough indicator): {w.rain48.toFixed(2)}</p><small className="muted">Source: Open-Meteo · Retrieved {new Date().toLocaleString()}</small></>}</div></>}
function Settings({data,update}:{data:FarmData;update:(p:Partial<FarmData>)=>void}){return <><Header title="Farm settings" subtitle="Your profile and farm location are stored in this browser."/><div className="card stack"><label>Farmer name<input className="field" value={data.farmer} onChange={e=>update({farmer:e.target.value})}/></label><label>Farm name<input className="field" value={data.farm} onChange={e=>update({farm:e.target.value})}/></label><label>City<input className="field" value={data.city} onChange={e=>update({city:e.target.value})}/></label><button className="secondary" onClick={()=>{const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='agrios-data.json';a.click();URL.revokeObjectURL(a.href)}}>Export farm data JSON</button><button className="secondary" onClick={()=>{const input=document.createElement('input');input.type='file';input.accept='application/json';input.onchange=async()=>{const f=input.files?.[0];if(f){try{const d=JSON.parse(await f.text());if(d.farmer&&Array.isArray(d.crops)&&Array.isArray(d.soil))update(d);else alert('Invalid AgriOS data file')}catch{alert('Could not read JSON file')}}};input.click()}}>Import farm data JSON</button></div></>}
export default App
