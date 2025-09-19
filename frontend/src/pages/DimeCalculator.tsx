import Header from "@/components/Header";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const DimeCalculator = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-md mx-auto">
          <div className="bg-white border border-gray-300 rounded-lg p-6">
            <h1 className="text-xl font-bold text-black mb-6">D.I.M.E. Calculator</h1>
            
            <form className="space-y-6">
              {/* Client Name */}
              <div>
                <Label htmlFor="clientName" className="text-black font-semibold">
                  Client Name:
                </Label>
                <Input
                  id="clientName"
                  type="text"
                  placeholder="Enter client's name"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Client Age */}
              <div>
                <Label htmlFor="clientAge" className="text-black font-semibold">
                  Client Age:
                </Label>
                <Input
                  id="clientAge"
                  type="number"
                  placeholder="Enter client's age"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Annual Income */}
              <div>
                <Label htmlFor="annualIncome" className="text-black font-semibold">
                  Your Annual Income:
                </Label>
                <Input
                  id="annualIncome"
                  type="number"
                  placeholder="Enter your annual income"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Years to Replace Income */}
              <div>
                <Label htmlFor="yearsToReplace" className="text-black font-semibold">
                  Number of Years to Replace Income:
                </Label>
                <Input
                  id="yearsToReplace"
                  type="number"
                  placeholder="e.g., 10, 20"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Mortgage Balance */}
              <div>
                <Label htmlFor="mortgageBalance" className="text-black font-semibold">
                  Outstanding Mortgage Balance:
                </Label>
                <Input
                  id="mortgageBalance"
                  type="number"
                  placeholder="Enter mortgage balance"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Current Debt */}
              <div>
                <Label htmlFor="currentDebt" className="text-black font-semibold">
                  Current Debt:
                </Label>
                <Input
                  id="currentDebt"
                  type="number"
                  placeholder="Enter current debt"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Education Expenses */}
              <div>
                <Label htmlFor="educationExpenses" className="text-black font-semibold">
                  Future Education Expenses (for children):
                </Label>
                <Input
                  id="educationExpenses"
                  type="number"
                  placeholder="Enter estimated education costs"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Final Expenses */}
              <div>
                <Label htmlFor="finalExpenses" className="text-black font-semibold">
                  Final Expenses (funeral, etc.):
                </Label>
                <Input
                  id="finalExpenses"
                  type="number"
                  placeholder="Enter estimated final expenses"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Existing Coverage */}
              <div>
                <Label htmlFor="existingCoverage" className="text-black font-semibold">
                  Existing Life Insurance Coverage:
                </Label>
                <Input
                  id="existingCoverage"
                  type="number"
                  placeholder="Enter current coverage amount"
                  className="mt-1 bg-white border border-gray-300 text-black placeholder-gray-500"
                />
              </div>

              {/* Calculate Button */}
              <div>
                <Button 
                  type="submit"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2"
                >
                  Calculate
                </Button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DimeCalculator;
