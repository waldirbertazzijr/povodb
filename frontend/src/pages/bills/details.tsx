import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Calendar, User, Vote, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { formatDate } from '@/lib/utils';
import Placeholder from '@/components/placeholder';

export default function BillDetailsPage() {
  const { id } = useParams<{ id: string }>();

  // This is a placeholder page, so we'll just use a placeholder component
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Link to="/bills">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="mr-1 h-4 w-4" />
            Back
          </Button>
        </Link>
        <h1 className="text-3xl font-bold tracking-tight">Bill Details</h1>
      </div>

      <Placeholder
        title="Bill Details Coming Soon"
        description="The bill details page is currently under development. Soon you'll be able to view detailed information about each bill, including sponsors, votes, and full text."
        icon={<FileText className="h-12 w-12 text-primary" />}
        returnPath="/bills"
        returnLabel="Back to Bills"
      />
    </div>
  );
}
