import { NextApiRequest, NextApiResponse } from "next";
import path from "path";
import { spawnSync } from "child_process";
import fs from "fs";

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

    const failedDownloads: string[] = [];

    try {
      // Folder output tempat menyimpan video
      const outputFolder = path.join(process.cwd(), "downloads");

      // Pastikan folder output ada
      if (!fs.existsSync(outputFolder)) {
        fs.mkdirSync(outputFolder, { recursive: true });
      }

      // Loop untuk mendownload setiap video
      for (let url of urls) {
        try {
          // Menyusun perintah yt-dlp
          const command = "yt-dlp";
          const args = [
            "-o",
            `${outputFolder}/%(title)s.%(ext)s`, // Template output
            url, // URL video yang ingin diunduh
          ];

          // Eksekusi perintah yt-dlp secara sinkron menggunakan spawnSync
          const result = spawnSync(
            "/Users/wahyudhafayash/Library/Python/3.9/bin/yt-dlp",
            args,
            {
              stdio: "pipe",
            }
          );

          // Jika ada error menjalankan yt-dlp
          if (result.error) {
            console.error(`Error running yt-dlp for ${url}:`, result.error);
            failedDownloads.push(url);
            continue;
          }

          console.log(
            `Download successful for ${url}: ${result.stdout.toString()}`
          );
        } catch (error: any) {
          console.error(
            `Error downloading video from ${url}: ${error.message}`
          );
          failedDownloads.push(url);
        }
      }

      // Jika ada video yang gagal didownload
      if (failedDownloads.length > 0) {
        return res.status(500).json({
          success: false,
          error: `Failed to download videos: ${failedDownloads.join(", ")}`,
        });
      }

      // Jika semua video berhasil didownload
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
