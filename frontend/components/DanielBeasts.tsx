'use client';

import { Crown, Shield, Swords, Scale } from 'lucide-react';

interface Kingdom {
  name: string;
  daniel2Symbol: string;
  daniel7Beast: string;
  daniel8Symbol: string;
  period: string;
  characteristics: string[];
  historicalFulfillment: string;
  color: string;
  icon: any;
}

const KINGDOMS: Kingdom[] = [
  {
    name: "Babylon",
    daniel2Symbol: "Head of Gold",
    daniel7Beast: "Lion with Eagle's Wings",
    daniel8Symbol: "Not mentioned (already reigning)",
    period: "605-539 BC",
    characteristics: [
      "Most glorious of all kingdoms",
      "Absolute monarchy under Nebuchadnezzar",
      "First universal empire",
      "Center of learning and architecture"
    ],
    historicalFulfillment: "Babylonian Empire under Nebuchadnezzar and successors. Daniel served in this kingdom. Known for Hanging Gardens, Tower of Babel reconstruction, and conquered Jerusalem in 586 BC.",
    color: "bg-yellow-500",
    icon: Crown
  },
  {
    name: "Medo-Persia",
    daniel2Symbol: "Chest and Arms of Silver",
    daniel7Beast: "Bear Raised on One Side",
    daniel8Symbol: "Ram with Two Horns",
    period: "539-331 BC",
    characteristics: [
      "Dual monarchy (Medes and Persians)",
      "Inferior to Babylon in glory",
      "Larger in extent",
      "Law of the Medes and Persians unchangeable"
    ],
    historicalFulfillment: "Cyrus the Great conquered Babylon in 539 BC. Issued decree allowing Jews to return and rebuild Jerusalem (Ezra 1:1-4). Empire stretched from India to Ethiopia. Fell to Alexander the Great in 331 BC.",
    color: "bg-gray-400",
    icon: Shield
  },
  {
    name: "Greece",
    daniel2Symbol: "Belly and Thighs of Bronze",
    daniel7Beast: "Leopard with Four Wings and Four Heads",
    daniel8Symbol: "Goat with Notable Horn, then Four Horns",
    period: "331-168 BC",
    characteristics: [
      "Swift conquest under Alexander",
      "Cultural and intellectual dominance",
      "Divided into four kingdoms after Alexander",
      "Hellenization of conquered territories"
    ],
    historicalFulfillment: "Alexander the Great conquered the known world by age 32. After his death (323 BC), empire divided among four generals: Cassander (Macedonia), Lysimachus (Thrace), Seleucus (Syria), Ptolemy (Egypt).",
    color: "bg-amber-600",
    icon: Swords
  },
  {
    name: "Rome",
    daniel2Symbol: "Legs of Iron, Feet of Iron and Clay",
    daniel7Beast: "Terrifying Beast with Iron Teeth and Ten Horns",
    daniel8Symbol: "Not explicitly mentioned (focus on horn from third kingdom)",
    period: "168 BC - 476 AD (Western), 1453 AD (Eastern)",
    characteristics: [
      "Strong as iron, crushing all opposition",
      "Divided into Western and Eastern empires",
      "Ten kingdoms emerge from Western empire",
      "Mix of strength (iron) and weakness (clay)"
    ],
    historicalFulfillment: "Roman Empire conquered Greece (Battle of Pydna, 168 BC). Crucified Jesus Christ during Tiberius Caesar. Destroyed Jerusalem in 70 AD. Western Rome fell in 476 AD, divided into ten kingdoms. Eastern (Byzantine) empire fell 1453 AD.",
    color: "bg-red-700",
    icon: Scale
  }
];

const TEN_HORNS = [
  { name: "Alemanni", modernName: "Germany" },
  { name: "Franks", modernName: "France" },
  { name: "Anglo-Saxons", modernName: "England" },
  { name: "Burgundians", modernName: "Switzerland" },
  { name: "Visigoths", modernName: "Spain" },
  { name: "Suevi", modernName: "Portugal" },
  { name: "Lombards", modernName: "Italy" },
  { name: "Heruli", modernName: "Uprooted 493 AD" },
  { name: "Vandals", modernName: "Uprooted 534 AD" },
  { name: "Ostrogoths", modernName: "Uprooted 538 AD" }
];

export default function DanielBeasts() {
  return (
    <div className="space-y-8">
      {/* Introduction */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-bold mb-4">Daniel's Prophetic Visions of World Kingdoms</h2>
        <p className="text-lg text-purple-100 leading-relaxed">
          The book of Daniel contains parallel prophetic visions revealing the succession of world empires from Babylon 
          to the end times. Three primary visions (Daniel 2, 7, and 8) describe the same historical sequence using 
          different symbolic representations: metals in a statue, beasts from the sea, and animals in conflict.
        </p>
        <p className="text-purple-100 mt-3">
          <strong>Historical fulfillment:</strong> These prophecies have been precisely fulfilled through history, 
          demonstrating the divine inspiration of Scripture and establishing confidence in yet-unfulfilled prophecies.
        </p>
      </div>

      {/* The Four Kingdoms */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {KINGDOMS.map((kingdom, idx) => {
          const Icon = kingdom.icon;
          return (
            <div key={idx} className="bg-white rounded-lg shadow-md border-t-4 overflow-hidden" style={{ borderColor: kingdom.color.replace('bg-', '') }}>
              <div className={`${kingdom.color} bg-opacity-10 p-6 border-b`}>
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <h3 className="text-2xl font-bold text-slate-900">{kingdom.name}</h3>
                    <p className="text-sm font-medium text-slate-600">{kingdom.period}</p>
                  </div>
                  <div className={`${kingdom.color} p-4 rounded-full`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                </div>
              </div>

              <div className="p-6 space-y-4">
                {/* Prophetic Symbols */}
                <div className="grid grid-cols-1 gap-3">
                  <div className="bg-slate-50 rounded p-3">
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Daniel 2 (Image)</div>
                    <div className="text-sm font-medium text-slate-800">{kingdom.daniel2Symbol}</div>
                  </div>
                  <div className="bg-slate-50 rounded p-3">
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Daniel 7 (Beasts)</div>
                    <div className="text-sm font-medium text-slate-800">{kingdom.daniel7Beast}</div>
                  </div>
                  <div className="bg-slate-50 rounded p-3">
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Daniel 8 (Symbols)</div>
                    <div className="text-sm font-medium text-slate-800">{kingdom.daniel8Symbol}</div>
                  </div>
                </div>

                {/* Characteristics */}
                <div>
                  <h4 className="text-sm font-bold text-slate-700 mb-2">Prophetic Characteristics:</h4>
                  <ul className="space-y-1">
                    {kingdom.characteristics.map((char, i) => (
                      <li key={i} className="flex items-start text-sm text-slate-600">
                        <span className="text-purple-500 mr-2">•</span>
                        <span>{char}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Historical Fulfillment */}
                <div className="bg-blue-50 border border-blue-200 rounded p-4">
                  <h4 className="text-sm font-bold text-blue-900 mb-2">Historical Fulfillment:</h4>
                  <p className="text-sm text-slate-700 leading-relaxed">{kingdom.historicalFulfillment}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* The Ten Horns / Kingdoms */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-slate-900 mb-4">The Ten Horns of Daniel 7</h3>
        <p className="text-slate-600 mb-6">
          Daniel 7:7-8 describes the fourth beast (Rome) with ten horns, representing ten kingdoms that emerged from 
          the divided Western Roman Empire. Three of these were uprooted by the papal power (the "little horn").
        </p>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {TEN_HORNS.map((horn, idx) => (
            <div 
              key={idx} 
              className={`p-4 rounded-lg border-2 text-center transition-all hover:shadow-md ${
                horn.modernName.includes('Uprooted') 
                  ? 'bg-red-50 border-red-300' 
                  : 'bg-slate-50 border-slate-300'
              }`}
            >
              <div className="font-bold text-slate-900 mb-1">{horn.name}</div>
              <div className={`text-xs ${
                horn.modernName.includes('Uprooted') 
                  ? 'text-red-600 font-semibold' 
                  : 'text-slate-600'
              }`}>
                {horn.modernName}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 bg-red-50 border border-red-200 rounded p-4">
          <h4 className="text-sm font-bold text-red-900 mb-2">The Three Uprooted Horns:</h4>
          <p className="text-sm text-slate-700 leading-relaxed">
            The Heruli (493 AD), Vandals (534 AD), and Ostrogoths (538 AD) were the three Arian kingdoms destroyed 
            by papal Rome. The final uprooting of the Ostrogoths in 538 AD marks the beginning of the 1260-year 
            period of papal supremacy, ending with the capture of Pope Pius VI in 1798 AD.
          </p>
        </div>
      </div>

      {/* The Little Horn */}
      <div className="bg-gradient-to-r from-red-600 to-purple-600 text-white rounded-lg shadow-lg p-6">
        <h3 className="text-2xl font-bold mb-4">The Little Horn Power (Daniel 7:8, 7:24-25)</h3>
        <div className="space-y-3 text-red-100">
          <p className="text-lg">
            <strong>Characteristics identified in prophecy:</strong>
          </p>
          <ul className="space-y-2 ml-6 list-disc">
            <li>Arises among the ten horns (from Western Rome's territory)</li>
            <li>Uproots three horns (Heruli, Vandals, Ostrogoths)</li>
            <li>Speaks pompous words against the Most High</li>
            <li>Persecutes the saints of the Most High</li>
            <li>Intends to change times and law</li>
            <li>Saints given into his hand for "time, times, and half a time" (1260 years)</li>
            <li>Power taken away at the end of the period</li>
          </ul>
          <p className="mt-4 text-white font-semibold">
            Historicist interpretation: The papal power system that dominated Europe from 538 AD to 1798 AD, 
            exactly 1260 years as prophesied.
          </p>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="bg-slate-800 text-white p-4">
          <h3 className="text-xl font-bold">Parallel Prophecies Comparison</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-100">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Kingdom</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Daniel 2</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Daniel 7</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Daniel 8</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Period</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {KINGDOMS.map((kingdom, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <div className="font-semibold text-slate-900">{kingdom.name}</div>
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-600">{kingdom.daniel2Symbol}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">{kingdom.daniel7Beast}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">{kingdom.daniel8Symbol}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">{kingdom.period}</td>
                </tr>
              ))}
              <tr className="hover:bg-slate-50 bg-yellow-50">
                <td className="px-4 py-3">
                  <div className="font-semibold text-slate-900">Divided Rome</div>
                </td>
                <td className="px-4 py-3 text-sm text-slate-600">Feet: Iron & Clay</td>
                <td className="px-4 py-3 text-sm text-slate-600">Ten Horns + Little Horn</td>
                <td className="px-4 py-3 text-sm text-slate-600">Horn from Greece area</td>
                <td className="px-4 py-3 text-sm text-slate-600">476 AD - Present</td>
              </tr>
              <tr className="hover:bg-slate-50 bg-green-50">
                <td className="px-4 py-3">
                  <div className="font-semibold text-slate-900">God's Kingdom</div>
                </td>
                <td className="px-4 py-3 text-sm text-slate-600">Stone cut without hands</td>
                <td className="px-4 py-3 text-sm text-slate-600">Kingdom given to Son of Man</td>
                <td className="px-4 py-3 text-sm text-slate-600">-</td>
                <td className="px-4 py-3 text-sm text-slate-600">Future - Eternal</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
