import React from 'react';
import { Vote } from 'lucide-react';
import Placeholder from '@/components/placeholder';

export default function VotesPage() {
  return (
    <Placeholder
      title="Voting Records"
      description="The voting records section is currently under development. Soon you'll be able to browse and search through voting records for politicians and bills."
      icon={<Vote className="h-12 w-12 text-primary" />}
      returnPath="/"
      returnLabel="Back to Home"
    />
  );
}
