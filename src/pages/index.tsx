import { useState } from "react";
import UrlInput from "@/pages/_components/UrlInput";

export default function Home() {
  const [urls, setUrls] = useState<string[]>([""]);
  const [status, setStatus] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setStatus("Downloading...");

    const urlList = urls.filter((url) => url.trim() !== "");

    if (urlList.length === 0) {
      setStatus("Please enter at least one URL.");
      return;
    }

    try {
      const res = await fetch("/api/download", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ urls: urlList }),
      });

      const data = await res.json();
      if (data.success) {
        setStatus("Download completed successfully!");
      } else {
        setStatus("Download failed. Please try again.");
      }
    } catch (error) {
      setStatus("Failed to connect to the server.");
    }
  };

  const handleUrlChange = (index: number, value: string) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  const addUrlInput = () => {
    setUrls([...urls, ""]);
  };

  const removeUrlInput = (index: number) => {
    if (urls.length > 1) {
      const newUrls = urls.filter((_, i) => i !== index);
      setUrls(newUrls);
    }
  };

  return (
    <section className="flex justify-center min-h-screen">
      <div className="pt-24">
        <h1 className="text-2xl mx-6 lg:mx-0 font-bold">
          TikTok, Twitter, Instagram Reels, and YouTube with Multiple Video
          Downloaders
        </h1>
        <form onSubmit={handleSubmit} className="mt-10 mx-5 lg:mx-0">
          {urls.map((url, index) => (
            <UrlInput
              key={index}
              url={url}
              index={index}
              onUrlChange={handleUrlChange}
              onAddUrl={addUrlInput}
              onRemoveUrl={removeUrlInput}
              isRemovable={urls.length > 1}
            />
          ))}

          <button
            type="submit"
            className="border p-2 rounded-lg bg-blue-400 text-white mt-4"
          >
            Download Videos
          </button>
        </form>
        <p className="mt-4">{status}</p>
      </div>
    </section>
  );
}
