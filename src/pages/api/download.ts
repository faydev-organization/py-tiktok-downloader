import { execSync } from "child_process";
import path from "path";
import { NextApiRequest, NextApiResponse } from "next";

interface DownloadRequestBody {
  urls: string[];
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === "POST") {
    const { urls }: DownloadRequestBody = req.body;

    if (!urls || urls.length === 0) {
      return res.status(400).json({
        success: false,
        error: "No URLs provided.",
      });
    }

    try {
      const pythonScriptPath = path.join(process.cwd(), "download_tiktok.py");

      // Loop through the list of URLs and download each video
      for (let url of urls) {
        try {
          // Execute the Python script synchronously
          const result = execSync(`python3 ${pythonScriptPath} "${url}"`);
          console.log(`Download successful for ${url}: ${result.toString()}`);
        } catch (error: any) {
          console.error(
            `Error downloading video from ${url}: ${error.message}`
          );
          return res.status(500).json({
            success: false,
            error: `Failed to download ${url}: ${error.message}`,
          });
        }
      }

      return res.status(200).json({ success: true });
    } catch (error: any) {
      console.error("Unexpected error:", error);
      return res.status(500).json({
        success: false,
        error: "Internal server error.",
      });
    }
  } else {
    return res.status(405).json({
      success: false,
      error: "Method not allowed",
    });
  }
}
