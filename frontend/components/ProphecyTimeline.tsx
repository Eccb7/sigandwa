'use client';

import { Calendar, Clock } from 'lucide-react';

interface PropheticPeriod {
  name: string;
  startYear: number;
  endYear: number;
  description: string;
  biblicalBasis: string;
  color: string;
}

const PROPHETIC_PERIODS: PropheticPeriod[] = [
  {
    name: "1260 Years of Papal Supremacy",
    startYear: 538,
    endYear: 1798,
    description: "Period of papal dominance from the fall of the Ostrogoths (538 AD) to the capture of Pope Pius VI by French General Berthier (1798 AD). Represents the 1260 prophetic days (years) mentioned seven times in Daniel and Revelation.",
    biblicalBasis: "Daniel 7:25, 12:7; Revelation 11:2-3, 12:6, 12:14, 13:5",
    color: "bg-red-500"
  },
  {
    name: "2300 Days to Cleansing",
    startYear: -457,
    endYear: 1844,
    description: "From the decree of Artaxerxes to rebuild Jerusalem (457 BC) to 1844 AD, marking 2300 prophetic years. Historicist interpretation sees 1844 as the beginning of the investigative judgment in heaven's sanctuary.",
    biblicalBasis: "Daniel 8:14",
    color: "bg-blue-500"
  },
  {
    name: "Seventy Weeks",
    startYear: -457,
    endYear: 34,
    description: "490 years (70 weeks × 7 days/week) from decree to rebuild Jerusalem to the stoning of Stephen and gospel to Gentiles. Includes Messiah's ministry and crucifixion at 483 years (69 weeks).",
    biblicalBasis: "Daniel 9:24-27",
    color: "bg-purple-500"
  },
  {
    name: "1290 Days",
    startYear: 508,
    endYear: 1798,
    description: "1290 prophetic years from the abolition of daily sacrifice and establishment of abomination of desolation. Some historicist scholars place this from 508 AD (establishment of papal power structures) to 1798 AD.",
    biblicalBasis: "Daniel 12:11",
    color: "bg-orange-500"
  },
  {
    name: "1335 Days",
    startYear: 508,
    endYear: 1843,
    description: "1335 prophetic years ending approximately at the time of the Great Disappointment (1843-1844). 'Blessed is the one who waits for and reaches the end of the 1335 days.'",
    biblicalBasis: "Daniel 12:12",
    color: "bg-green-500"
  }
];

export default function ProphecyTimeline() {
  const minYear = Math.min(...PROPHETIC_PERIODS.map(p => p.startYear));
  const maxYear = Math.max(...PROPHETIC_PERIODS.map(p => p.endYear));
  const totalYears = maxYear - minYear;

  const getPosition = (year: number) => {
    return ((year - minYear) / totalYears) * 100;
  };

  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-slate-900 mb-4 flex items-center">
          <Clock className="w-6 h-6 mr-2 text-purple-600" />
          Historicist Prophetic Timeline
        </h3>
        <p className="text-slate-600 mb-6">
          Based on the year-day principle (Ezekiel 4:6, Numbers 14:34), where one prophetic day represents one literal year. 
          This timeline shows major prophetic periods as understood by the historicist school of Biblical interpretation.
        </p>

        {/* Visual Timeline */}
        <div className="relative h-32 bg-slate-100 rounded-lg mb-8">
          {/* Timeline axis */}
          <div className="absolute inset-0 flex items-center px-4">
            <div className="w-full h-1 bg-slate-300" />
          </div>

          {/* Year markers */}
          <div className="absolute inset-0 flex justify-between items-end px-4 pb-2">
            <div className="text-xs text-slate-600 font-medium">457 BC</div>
            <div className="text-xs text-slate-600 font-medium">1 AD</div>
            <div className="text-xs text-slate-600 font-medium">538 AD</div>
            <div className="text-xs text-slate-600 font-medium">1798 AD</div>
            <div className="text-xs text-slate-600 font-medium">1844 AD</div>
          </div>

          {/* Period markers */}
          {PROPHETIC_PERIODS.map((period, idx) => {
            const start = getPosition(period.startYear);
            const end = getPosition(period.endYear);
            const width = end - start;

            return (
              <div
                key={idx}
                className="absolute top-8 h-8 rounded-full opacity-60 hover:opacity-90 transition-opacity cursor-pointer"
                style={{
                  left: `${start}%`,
                  width: `${width}%`,
                }}
                title={period.name}
              >
                <div className={`${period.color} h-full rounded-full`} />
              </div>
            );
          })}
        </div>
      </div>

      {/* Period Details */}
      <div className="grid grid-cols-1 gap-6">
        {PROPHETIC_PERIODS.map((period, idx) => (
          <div key={idx} className="bg-white rounded-lg shadow-md p-6 border-l-4" style={{ borderColor: period.color.replace('bg-', '') }}>
            <div className="flex items-start justify-between mb-3">
              <div>
                <h4 className="text-lg font-bold text-slate-900">{period.name}</h4>
                <div className="flex items-center text-sm text-slate-500 mt-1">
                  <Calendar className="w-4 h-4 mr-1" />
                  <span>
                    {period.startYear < 0 ? `${Math.abs(period.startYear)} BC` : `${period.startYear} AD`} - 
                    {period.endYear < 0 ? `${Math.abs(period.endYear)} BC` : `${period.endYear} AD`}
                  </span>
                  <span className="ml-3 text-slate-400">
                    ({Math.abs(period.endYear - period.startYear)} years)
                  </span>
                </div>
              </div>
              <div className={`${period.color} w-12 h-12 rounded-lg opacity-20`} />
            </div>

            <p className="text-slate-700 mb-3 leading-relaxed">{period.description}</p>

            <div className="bg-slate-50 rounded p-3">
              <div className="flex items-center text-xs font-semibold text-slate-600 mb-1">
                <span className="uppercase tracking-wide">Biblical Basis:</span>
              </div>
              <div className="text-sm text-slate-700">{period.biblicalBasis}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Year-Day Principle Explanation */}
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
        <h4 className="text-lg font-bold text-purple-900 mb-3">The Year-Day Principle</h4>
        <div className="space-y-3 text-slate-700">
          <p>
            The historicist interpretation of Bible prophecy applies the year-day principle, where symbolic time periods 
            represent literal years rather than literal days. This principle is derived from explicit Biblical statements:
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4">
            <li>
              <strong>Numbers 14:34</strong> - "After the number of the days in which ye searched the land, even forty days, 
              each day for a year, shall ye bear your iniquities, even forty years."
            </li>
            <li>
              <strong>Ezekiel 4:6</strong> - "I have appointed thee each day for a year."
            </li>
          </ul>
          <p className="mt-4">
            This principle was recognized by early church fathers and Protestant Reformers including Joachim of Calabria (12th century), 
            Isaac Newton, and William Miller. It explains the precise fulfillment of prophetic timelines like the 1260 years 
            of papal supremacy (538-1798 AD) and the 2300 years ending in 1844 AD.
          </p>
        </div>
      </div>
    </div>
  );
}
