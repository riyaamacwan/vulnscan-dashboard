export default function SeverityCard({ findings }) {
  const counts = findings.reduce((acc, finding) => {
    acc[finding.severity] = (acc[finding.severity] || 0) + 1;
    return acc;
  }, {});

  const levels = ["critical", "high", "medium", "low", "info"];

  return (
    <div className="grid grid-cols-5 gap-4">
      {levels.map((level) => (
        <div key={level} className="p-4 bg-white rounded-xl shadow">
          <p className="text-sm uppercase text-gray-500">{level}</p>
          <p className="text-2xl font-bold">{counts[level] || 0}</p>
        </div>
      ))}
    </div>
  );
}