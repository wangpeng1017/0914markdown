"use client";

import { useState, useRef, useCallback } from "react";

interface ConversionResult {
  success: boolean;
  markdown?: string;
  filename?: string;
  error?: string;
}

export function FileUploadComponent() {
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ConversionResult | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, []);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/convert", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch {
      setResult({
        success: false,
        error: "Network error: Failed to upload file",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (result?.markdown && result?.filename) {
      const blob = new Blob([result.markdown], { type: "text/markdown" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = result.filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const handleReset = () => {
    setResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {!result && (
        <div
          className={`
            relative border-2 border-dashed rounded-lg p-12 text-center transition-all duration-200
            ${isDragging
              ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20"
              : "border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500"
            }
            ${isLoading ? "opacity-50 pointer-events-none" : ""}
          `}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            onChange={handleFileSelect}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            accept=".txt,.html,.htm,.csv,.pdf,.docx,.xlsx,.pptx"
            disabled={isLoading}
          />
          
          {isLoading ? (
            <div className="animate-pulse">
              <div className="w-16 h-16 bg-blue-500 rounded-full mx-auto mb-4 animate-pulse-slow"></div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Converting your file...
              </h3>
              <p className="text-gray-500 dark:text-gray-400">
                This may take a few moments
              </p>
            </div>
          ) : (
            <>
              <div className="w-16 h-16 bg-gray-400 dark:bg-gray-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                {isDragging ? "Drop your file here" : "Upload a file"}
              </h3>
              <p className="text-gray-500 dark:text-gray-400 mb-4">
                Drag and drop or click to select a file
              </p>
              <div className="text-sm text-center">
                <p className="text-gray-400 dark:text-gray-500 mb-2">
                  Supports TXT, HTML, CSV, PDF, Word, Excel, PowerPoint files
                </p>
                <p className="text-blue-500 dark:text-blue-400 text-xs">
                  ✨ Enhanced version - PDF, Word, Excel now supported!
                </p>
              </div>
            </>
          )}
        </div>
      )}

      {result && (
        <div className="animate-fade-in">
          {result.success ? (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
              {/* Header */}
              <div className="bg-gray-50 dark:bg-gray-700 px-6 py-4 flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                    Conversion Complete
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {result.filename}
                  </p>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={handleDownload}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                  >
                    Download
                  </button>
                  <button
                    onClick={handleReset}
                    className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                  >
                    New File
                  </button>
                </div>
              </div>

              {/* Preview */}
              <div className="p-6">
                <h4 className="text-md font-medium text-gray-900 dark:text-white mb-4">
                  Markdown Preview:
                </h4>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 max-h-96 overflow-auto">
                  <pre className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap font-mono">
                    {result.markdown}
                  </pre>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 animate-slide-up">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center mr-4">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-medium text-red-800 dark:text-red-200">
                    Conversion Failed
                  </h3>
                  <p className="text-red-600 dark:text-red-300 mt-1">
                    {result.error}
                  </p>
                </div>
                <button
                  onClick={handleReset}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Try Again
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}