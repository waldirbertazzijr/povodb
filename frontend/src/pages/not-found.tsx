import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-center px-4">
      <h1 className="text-9xl font-extrabold text-gray-700 dark:text-gray-300">404</h1>
      <div className="absolute rotate-12 rounded-full bg-primary/10 px-2 text-sm text-primary">
        Page Not Found
      </div>
      <div className="mt-8">
        <div className="text-3xl font-bold">Oops! Page not found</div>
        <div className="mt-4 text-lg text-gray-500 dark:text-gray-400">
          The page you are looking for doesn't exist or has been moved.
        </div>
        <div className="mt-6">
          <Link to="/">
            <Button>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Home
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
