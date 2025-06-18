import { useState, useEffect } from 'react';
import locations from './locations.json';

function LocationInput({ value, onChange }) {
  const [input, setInput] = useState(value || '');
  const [filtered, setFiltered] = useState([]);

  useEffect(() => {
    setInput(value || ''); 
  }, [value]);

  useEffect(() => {
    if (input.trim() === '') {
      setFiltered([]);
    } else {
      setFiltered(
        locations.filter((loc) =>
          loc.toLowerCase().includes(input.toLowerCase())
        )
      );
    }
  }, [input]);

  const handleSelect = (loc) => {
    setInput(loc);
    setFiltered([]);
    onChange(loc); 
  };

  return (
    <div className="relative">
      <label className="block text-white mb-2">Location :</label>
      <input
        type="text"
        value={input}
        onChange={(e) => {
          setInput(e.target.value);
          onChange(e.target.value); 
        }}
        placeholder="Enter Location"
        className="rounded-xl bg-slate-700/50 border-2 w-[500px] hover:bg-slate-500 border-white text-white px-4 py-2"
      />
      {filtered.length > 0 && (
        <ul className="absolute bg-slate-800 text-white mt-1 rounded-xl w-[600px] max-h-40 overflow-y-auto shadow-lg z-10">
          {filtered.map((loc, i) => (
            <li
              key={i}
              className="px-4 py-2 hover:bg-slate-600 cursor-pointer"
              onClick={() => handleSelect(loc)}
            >
              {loc}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default LocationInput;
