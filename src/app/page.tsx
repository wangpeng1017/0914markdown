"use client";

import { FileUploadComponent } from "@/components/FileUpload";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Markdown Converter
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Convert documents to Markdown instantly. 
            Enhanced version supporting PDF, Word, Excel, PowerPoint, TXT, HTML, and CSV files.
          </p>
        </div>
        
        {/* Main Content */}
        <FileUploadComponent />
        
        {/* Footer */}
        <div className="text-center mt-16 text-sm text-gray-500 dark:text-gray-400">
          <p>
            Powered by{" "}
            <a 
              href="https://github.com/microsoft/markitdown" 
              target="_blank" 
              rel="noopener noreferrer"
              className="underline hover:text-gray-700 dark:hover:text-gray-300"
            >
              Microsoft MarkItDown
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
