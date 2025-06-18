import React from 'react';

function FacingDirectionSelect({ value, onChange }) {
  const directions = [
    'East',
    'South-East',
    'West',
    'South',
    'North',
    'North-East',
    'South-West',
    'North-West',
  ];

  return (
    <div className="mb-4">
      <label className="block text-white mb-2">Facing Direction :</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-xl bg-slate-700/50 border-2 hover:bg-slate-500 border-white text-white px-4 py-2 w-[300px]"
      >
        <option value="">Select Direction</option>
        {directions.map((dir) => (
          <option key={dir} value={dir}>
            {dir}
          </option>
        ))}
      </select>
    </div>
  );
}

export default FacingDirectionSelect;
