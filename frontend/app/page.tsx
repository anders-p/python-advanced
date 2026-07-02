"use client";

import React, { useEffect, useState } from "react";
import Script from "next/script";

import RadioSelect from "@/components/RadioSelect"

// Define a type for the global window object to include Bokeh safely in TypeScript
declare global {
  interface Window {
    Bokeh?: any;
  }
}

export default function BokehChartPage() {
  const [bokehLoaded, setBokehLoaded] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedPeriod, setSelectedPeriod] = useState("W")
  const periodOptions = ["D", "W", "ME", "QE", "YE"]

  useEffect(() => {
    // Only fetch the chart data once the BokehJS script has finished loading
    if (!bokehLoaded) return;

    const fetchAndRenderChart = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `http://127.0.0.1:8000/chart/sales?period=${selectedPeriod}`
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch chart data: ${response.statusText}`);
        }

        const chartJson = await response.json();

        // Clear previous content in the container if any, to prevent duplicate renders
        const container = document.getElementById("bokeh-chart");
        if (container) container.innerHTML = "";

        // Embed the chart using the global Bokeh library loaded via next/script
        if (window.Bokeh) {
          window.Bokeh.embed.embed_item(chartJson);
        } else {
          throw new Error("BokehJS library is not available on the window object.");
        }

        setError(null);
      } catch (err: any) {
        console.error("Error rendering Bokeh chart:", err);
        setError(err.message || "An unexpected error occurred.");
      } finally {
        setLoading(false);
      }
    };

    fetchAndRenderChart();
  }, [bokehLoaded, selectedPeriod]);

  // When user selects a different period
  const handlePeriodChange = (newPeriod: string) => {
    setSelectedPeriod(newPeriod)
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      {/* 1. Load the official BokehJS script from CDN */}
      {/* Note: Ensure the version (e.g., 3.4.1) roughly matches your Python bokeh package version */}
      <Script
        src="https://cdn.bokeh.org/bokeh/release/bokeh-3.9.1.min.js"
        strategy="afterInteractive"
        onLoad={() => setBokehLoaded(true)}
        onError={() => setError("Could not load the BokehJS CDN script.")}
      />

      <h2>Next.js Analytics Dashboard</h2>
      <p>Displaying data pulled dynamically from FastAPI.</p>

      <hr style={{ margin: "1.5rem 0", borderColor: "#eaeaea" }} />

      {/* 2. Loading and Error States */}
      {loading && <p style={{ color: "#666" }}>Loading chart visualization...</p>}
      {error && <p style={{ color: "#ef4444" }}><strong>Error:</strong> {error}</p>}

      {/* 3. The target wrapper. The ID *must* match the target string specified in your python script */}
      <div
        id="bokeh-chart"
        style={{
          minHeight: "400px",
          display: loading ? "none" : "block",
          marginTop: "1rem"
        }}
      />
      <RadioSelect
        title="Select Metric"
        options={periodOptions}
        selectedValue={selectedPeriod}
        onChange={handlePeriodChange}
      />

      <div className="text-sm text-gray-500">
        The backend is now filtering data for: <strong className="text-gray-800">{selectedPeriod}</strong>
      </div>
    </div>
  );
}


// import Image from "next/image";

// export default function Home() {
//   return (
//     <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black">
//       <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
//         <Image
//           className="dark:invert"
//           src="/next.svg"
//           alt="Next.js logo"
//           width={100}
//           height={20}
//           priority
//         />
//         <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
//           <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
//             To get started, edit the page.tsx file.
//           </h1>
//           <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
//             Looking for a starting point or more instructions? Head over to{" "}
//             <a
//               href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//               className="font-medium text-zinc-950 dark:text-zinc-50"
//             >
//               Templates
//             </a>{" "}
//             or the{" "}
//             <a
//               href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//               className="font-medium text-zinc-950 dark:text-zinc-50"
//             >
//               Learning
//             </a>{" "}
//             center.
//           </p>
//         </div>
//         <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
//           <a
//             className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
//             href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             <Image
//               className="dark:invert"
//               src="/vercel.svg"
//               alt="Vercel logomark"
//               width={16}
//               height={16}
//             />
//             Deploy Now
//           </a>
//           <a
//             className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
//             href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Documentation
//           </a>
//         </div>
//       </main>
//     </div>
//   );
// }
