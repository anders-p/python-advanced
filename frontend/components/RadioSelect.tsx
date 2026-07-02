'use client';

interface RadioSelectProps {
  options: string[];
  selectedValue: string;
  onChange: (value: string) => void;
  title?: string;
}

export default function RadioSelect({
  options,
  selectedValue,
  onChange,
  title
}: RadioSelectProps) {
  return (
    <div className="w-full max-w-sm p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
      {title && (
        <h3 className="text-sm font-semibold text-gray-700 mb-3">
          {title}
        </h3>
      )}

      <div className="space-y-2">
        {options.map((option) => {
          const isChecked = selectedValue === option;

          return (
            <label
              key={option}
              className={`flex items-center px-4 py-3 border rounded-lg cursor-pointer transition-all duration-150 text-sm font-medium ${
                isChecked
                  ? 'border-blue-600 bg-blue-50/40 text-blue-900'
                  : 'border-gray-200 bg-white hover:bg-gray-50 text-gray-600'
              }`}
            >
              <input
                type="radio"
                name="generic-radio-group"
                value={option}
                checked={isChecked}
                onChange={() => onChange(option)}
                className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="ml-3 capitalize">
                {option.replace(/[-_]/g, ' ')} {/* Cleans up strings like 'total_sales' to 'total sales' */}
              </span>
            </label>
          );
        })}
      </div>
    </div>
  );
}
