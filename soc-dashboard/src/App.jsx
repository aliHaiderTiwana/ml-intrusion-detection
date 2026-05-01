import React, { useState, useEffect } from 'react';

export default function App() {
  const [logs, setLogs] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to your FastAPI Python server
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = () => {
      console.log("Connected to AI Brain");
      setIsConnected(true);
    };

    ws.onclose = () => {
      console.log("Disconnected from AI Brain");
      setIsConnected(false);
    };

    ws.onmessage = (event) => {
      const incomingPacket = JSON.parse(event.data);
      setLogs((prevLogs) => [incomingPacket, ...prevLogs].slice(0, 50));
    };

    return () => ws.close();
  }, []);

  const totalPackets = logs.length;
  const totalAttacks = logs.filter(log => log.prediction === "Attack").length;

  return (
    <div className="min-h-screen p-8 font-sans">
      
      {/* Header Section */}
      <div className="flex justify-between items-center mb-8 border-b border-slate-700 pb-4">
        <div>
          <h1 className="text-3xl font-bold text-cyan-400 tracking-wider">AUTONOMOUS IDS</h1>
          <p className="text-slate-400 text-sm mt-1">Lead Architect: Ali Haider | Abdullah | Real-Time SOC</p>
        </div>
        <div className="flex items-center gap-3">
          <div className={`h-3 w-3 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="text-slate-300 font-mono text-sm">
            {isConnected ? "SYSTEM ACTIVE" : "SYSTEM OFFLINE"}
          </span>
        </div>
      </div>

      {/* Metrics Dashboards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg">
          <h2 className="text-slate-400 text-sm uppercase tracking-widest mb-2">Live Packets Analyzed</h2>
          <p className="text-4xl font-light text-white">{totalPackets}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-lg border border-red-900/50 shadow-lg">
          <h2 className="text-red-400 text-sm uppercase tracking-widest mb-2">Threats Blocked</h2>
          <p className="text-4xl font-bold text-red-500">{totalAttacks}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg">
          <h2 className="text-slate-400 text-sm uppercase tracking-widest mb-2">AI Engine Status</h2>
          <p className="text-xl font-mono text-cyan-400 mt-2">Random Forest (v1.0)</p>
        </div>
      </div>

      {/* Live Traffic Table */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden shadow-2xl">
        <div className="p-4 border-b border-slate-700 bg-slate-900/50">
          <h2 className="text-lg font-semibold text-slate-200">Live Network Traffic</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900/80 text-slate-400 text-xs uppercase tracking-wider">
                <th className="p-4 font-medium">Timestamp</th>
                <th className="p-4 font-medium">Source IP</th>
                <th className="p-4 font-medium">Packet Size</th>
                <th className="p-4 font-medium">AI Classification</th>
              </tr>
            </thead>
            <tbody className="text-sm font-mono divide-y divide-slate-700">
              {logs.length === 0 ? (
                <tr>
                  <td colSpan="4" className="p-8 text-center text-slate-500 italic">
                    Awaiting network traffic...
                  </td>
                </tr>
              ) : (
                logs.map((log, index) => (
                  <tr key={index} className="hover:bg-slate-700/50 transition-colors">
                    <td className="p-4 text-slate-300">{log.timestamp}</td>
                    <td className="p-4 text-cyan-300">{log.source_ip}</td>
                    <td className="p-4 text-slate-400">{log.packet_size} bytes</td>
                    <td className="p-4">
                      {log.prediction === "Attack" ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-red-500/20 text-red-400 border border-red-500/30">
                          🚨 ATTACK
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                          ✓ NORMAL
                        </span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}