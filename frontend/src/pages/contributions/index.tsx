import React from 'react';
import { Coins } from 'lucide-react';
import Placeholder from '@/components/placeholder';

export default function ContributionsPage() {
  return (
    <Placeholder
      title="Political Contributions"
      description="The political contributions section is currently under development. Soon you'll be able to explore financial contributions to political campaigns and track the money in politics."
      icon={<Coins className="h-12 w-12 text-primary" />}
      returnPath="/"
      returnLabel="Back to Home"
    />
  );
}
