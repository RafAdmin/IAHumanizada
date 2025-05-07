import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";

// Placeholder for authentication check - in a real app, this would be protected

export default function DashboardPage() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100 dark:bg-gray-900">
      {/* Basic Header */} 
      <header className="sticky top-0 z-10 flex items-center justify-between h-16 px-4 border-b bg-background md:px-6">
        <h1 className="text-lg font-semibold">IA Humanizada - Dashboard</h1>
        {/* Add Logout button or user menu later */}
        <Button variant="outline" size="sm">Logout</Button>
      </header>

      {/* Main Content Area */} 
      <main className="flex-1 p-4 md:p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Meus Agentes</h2>
          <Link href="/dashboard/agents/new"> {/* Link to future creation page */} 
            <Button>Criar Novo Agente</Button>
          </Link>
        </div>

        {/* Placeholder for Agent List */} 
        <Card>
          <CardHeader>
            <CardTitle>Lista de Agentes</CardTitle>
            <CardDescription>Aqui você verá seus agentes criados.</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Nenhum agente criado ainda. Clique em "Criar Novo Agente" para começar.
            </p>
            {/* Later, map through agents data here */}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}

