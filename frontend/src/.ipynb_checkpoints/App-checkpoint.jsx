import { useState } from 'react';
import LocationInput from './components/location';
import FacingDirectionSelect from './components/facing';
import TitleBar from './components/titlebar';

function App() {
  const [location, setLocation] = useState('');
  const [facing, setFacing] = useState('');
  const [bhk, setBhk] = useState(1);
  const [bathroom, setBathroom] = useState(1);
  const [roadAccess, setRoadAccess] = useState(5);
  const [parking, setParking] = useState(1);
  const [landArea, setLandArea] = useState(20);
  const [predictedPrice, setPredictedPrice] = useState('');

  const handlePredict = async () => {
    const data = {
      road_access: roadAccess,
      facing: facing,
      parking: parking,
      bathroom: bathroom,
      location: location,
      land_area_sq_m: landArea,
      bhk: bhk
    };

    try {
      const res = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await res.json();
      setPredictedPrice(`Rs. ${result.predicted_price.toFixed(2)}` + '  Cr');
    } catch (err) {
      console.error('Prediction error:', err);
      setPredictedPrice('Error predicting price');
    }
  };

  return (
    <div className="bg-slate-950 min-h-screen text-white">
      <TitleBar />

      <div className="flex justify-center items-center pt-20">
        <div className="bg-slate-800 rounded-xl shadow-lg text-sky-300 text-2xl p-8 w-[600px]">
          <h2 className="font-bold mb-6 text-white">Enter Details</h2>

          <div>
            <LocationInput value={location} onChange={setLocation} />
          </div>

          <div className='mt-6'>
            <FacingDirectionSelect value={facing} onChange={setFacing} />
          </div>

          <div className='flex flex-row'>
            <div className="mt-6 mr-14">
              <label className="block text-white mb-2">BHK :</label>
              <input
                type="number"
                min="1"
                max="20"
                step="1"
                value={bhk}
                onChange={(e) => setBhk(Number(e.target.value))}
                className="rounded-xl bg-slate-700/50 border-2 w-[200px] border-white hover:bg-slate-500 text-white px-4 py-2"
              />
            </div>
            <div className="mt-6">
              <label className="block text-white mb-2">Bath :</label>
              <input
                type="number"
                min="1"
                max="20"
                step="1"
                value={bathroom}
                onChange={(e) => setBathroom(Number(e.target.value))}
                className="rounded-xl bg-slate-700/50 border-2 w-[200px] hover:bg-slate-500  border-white text-white px-4 py-2"
              />
            </div>
          </div>

          <div className='flex flex-row'>
            <div className="mt-6 mr-14">
              <label className="block text-white mb-2">Road Access (in m):</label>
              <input
                type="number"
                min="1"
                max="20"
                step="1"
                value={roadAccess}
                onChange={(e) => setRoadAccess(Number(e.target.value))}
                className="rounded-xl bg-slate-700/50 border-2 w-[200px] hover:bg-slate-500 border-white text-white px-4 py-2"
              />
            </div>
            <div className="mt-6">
              <label className="block text-white mb-2">No of Parking :</label>
              <input
                type="number"
                min="0"
                max="10"
                step="1"
                value={parking}
                onChange={(e) => setParking(Number(e.target.value))}
                className="rounded-xl bg-slate-700/50 border-2 hover:bg-slate-500 w-[200px] border-white text-white px-4 py-2"
              />
            </div>
          </div>

          <div className='flex flex-row'>
            <div className="mt-6 mr-14">
              <label className="block text-white mb-2">Land Area (sq. m):</label>
              <input
                type="number"
                min="20"
                step="10"
                value={landArea}
                onChange={(e) => setLandArea(Number(e.target.value))}
                className="rounded-xl bg-slate-700/50 border-2 w-[300px] hover:bg-slate-500 border-white text-white px-4 py-2"
              />
            </div>
          </div>

          <div className='flex flex-row'>
            <div className="flex flex-col mt-14">
              <label className="block text-white mb-2">Predicted Price:</label>
              <input
                readOnly
                value={predictedPrice}
                className="rounded-xl bg-slate-700/50 border-2 w-[400px] border-white text-white px-4 py-2"
                placeholder='Predicted Price'
              />
            </div>
            <button
              onClick={handlePredict}
              className="px-4 py-2 bg-slate-700/50 border-2 w-[180px] border-white hover:bg-slate-500 h-12 mt-24 rounded-xl ml-5 text-white"
            >
              Calculate
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
