"use client";
import { useState } from "react";
import { BiCopy } from "react-icons/bi";
import { GoDownload, GoUpload } from "react-icons/go";
import axios from "axios";
import { VscLoading } from "react-icons/vsc";

const ChooseFile = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.length) {
      return; // if there is no file, do nothing
    }
    const selectedFile = e.target.files[0];

    if (selectedFile && selectedFile.type === "video/mp4") {
      setFile(selectedFile); // Set file
    } else {
      alert("Please upload a valid .mp4 file.");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("No file selected for upload.");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    try {
      setLoading(true);
      await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded / progressEvent.total!) * 100
          );
          console.log(`Upload Progress: ${progress}%`);
        },
      });
      alert("File uploaded successfully!");

    } catch (error) {
      setLoading(false);
      console.error("Error uploading file:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div
        onClick={() => {
          document.getElementById("fileInput")?.click();
        }}
        className={`cursor-pointer flex gap-2 mx-auto items-center rounded-md bg-slate-800 py-2 px-4 border border-transparent text-base text-white shadow-md hover:shadow-lg focus:bg-slate-700 focus:shadow-none active:bg-slate-700 hover:bg-slate-700 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none w-fit`}
      >
        <BiCopy size={20} />
        <input
          type="file"
          disabled={loading}
          accept="video/mp4"
          onChange={handleFileChange}
          className="hidden"
          id="fileInput"
        />
        {file ? (
          <div className="flex gap-5">
            <span>Chosen file</span>
            <span>{file.name}</span>
          </div>
        ) : (
          <button className="text-sm font-medium" disabled={loading}>
            Choose a Video File
          </button>
        )}
      </div>
      <div className="flex justify-center mt-20 gap-4">
        <button
          onClick={handleUpload}
          disabled={loading}
          className={`cursor-pointer flex gap-2 items-center rounded-md bg-slate-800 py-2 px-4 border border-transparent text-base text-white shadow-md hover:shadow-lg focus:bg-slate-700 focus:shadow-none active:bg-slate-700 hover:bg-slate-700 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none w-2/12`}
        >
          <span className="text-md font-medium flex gap-2">
            {loading ? (
              <section className="flex  justify-center items-center">
                <VscLoading className="mr-2 animate-spin" />
                <span> Processing...</span>
              </section>
            ) : (
              <>
                <GoUpload size={20} />
                Encrypt and Upload
              </>
            )}
          </span>
        </button>

        <div
          className={`cursor-pointer flex gap-2 items-center rounded-md bg-slate-800 py-2 px-4 border border-transparent text-base text-white shadow-md hover:shadow-lg focus:bg-slate-700 focus:shadow-none active:bg-slate-700 hover:bg-slate-700 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none w-1/6`}
        >
          <GoDownload size={20} />
          <button className="text-md font-medium">Download</button>
        </div>
      </div>
    </>
  );
};

export default ChooseFile;
