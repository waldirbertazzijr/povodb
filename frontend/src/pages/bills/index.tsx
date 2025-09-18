import React from 'react';
import { FileText } from 'lucide-react';
import Placeholder from '@/components/placeholder';

export default function BillsPage() {
  return (
    <Placeholder
      title="Bills Database"
      description="The bills database is currently under development. Soon you'll be able to browse and search through legislative bills, their sponsors, and voting records."
      icon={<FileText className="h-12 w-12 text-primary" />}
      returnPath="/"
      returnLabel="Back to Home"
    />
  );
}
