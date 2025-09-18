import React, { useState } from 'react';
import { X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface DebugPanelProps {
  data?: any;
  error?: Error | null;
  isLoading?: boolean;
  query?: string;
}

export default function DebugPanel({ data, error, isLoading, query }: DebugPanelProps) {
  const [isOpen, setIsOpen] = useState(false);

  if (!isOpen) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <Button
          size="sm"
          variant="secondary"
          onClick={() => setIsOpen(true)}
          className="bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300"
        >
          Debug Panel
        </Button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-0 right-0 w-full md:w-1/2 lg:w-1/3 h-1/2 bg-black/90 text-white z-50 p-4 overflow-auto rounded-t-lg border border-amber-500">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-amber-400 font-bold">Debug Panel</h3>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => setIsOpen(false)}
          className="text-white hover:bg-gray-800"
        >
          <X className="h-4 w-4" />
        </Button>
      </div>

      <div className="space-y-2 text-xs font-mono">
        {isLoading && (
          <div className="bg-blue-900/50 p-2 rounded">
            <p className="text-blue-300">Loading...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-900/50 p-2 rounded">
            <p className="text-white font-semibold">Error:</p>
            <pre className="text-red-300 mt-1 whitespace-pre-wrap overflow-auto max-h-20">
              {error.message}
            </pre>
            <pre className="text-red-400 mt-1 whitespace-pre-wrap overflow-auto max-h-40">
              {error.stack}
            </pre>
          </div>
        )}

        {query && (
          <div className="bg-purple-900/50 p-2 rounded">
            <p className="text-white font-semibold">Query:</p>
            <pre className="text-purple-300 mt-1 whitespace-pre-wrap">{query}</pre>
          </div>
        )}

        {data && (
          <div className="bg-green-900/50 p-2 rounded">
            <p className="text-white font-semibold">Response Data:</p>
            <pre className="text-green-300 mt-1 whitespace-pre-wrap overflow-auto max-h-60">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
