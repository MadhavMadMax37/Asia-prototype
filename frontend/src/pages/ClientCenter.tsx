import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Header from "@/components/Header";

const ClientCenter = () => {
  const accountFeatures = [
    {
      title: "Get ID Cards",
      icon: "🆔"
    },
    {
      title: "Request For Change", 
      icon: "📝"
    },
    {
      title: "Make Payments",
      icon: "💳"
    },
    {
      title: "Get Certificates",
      icon: "📄"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <section className="py-12 bg-gray-100 min-h-[90vh] flex items-center">
        <div className="container mx-auto px-4">
          <div className="max-w-5xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-0 bg-white rounded-lg shadow-lg overflow-hidden">
              
              {/* Left Side - Welcome Section */}
              <div className="bg-gradient-to-br from-blue-400 to-blue-600 p-8 text-white">
                <div className="mb-8">
                  <p className="text-blue-100 text-sm font-medium mb-2 tracking-wide">WELCOME</p>
                  <h1 className="text-2xl font-bold leading-tight">
                    Manage your insurance account anytime, anywhere
                  </h1>
                </div>
                
                <div className="space-y-3">
                  {accountFeatures.map((feature, index) => (
                    <div key={index} className="flex items-center space-x-4 p-3 bg-black/20 rounded-md">
                      <div className="w-8 h-8 bg-white/20 rounded flex items-center justify-center text-lg">
                        {feature.icon}
                      </div>
                      <h3 className="font-medium text-white">{feature.title}</h3>
                    </div>
                  ))}
                </div>
              </div>

              {/* Right Side - Sign In Form */}
              <div className="p-8 bg-white">
                <div className="text-center mb-8">
                  <div className="w-16 h-16 bg-gradient-to-br from-brand-orange to-brand-blue rounded-full mx-auto mb-4 flex items-center justify-center">
                    <span className="text-white font-bold text-xl">🏢</span>
                  </div>
                  <h2 className="text-lg font-semibold text-gray-700 mb-1">
                    Sign-in to Client Center
                  </h2>
                </div>

                <form className="space-y-4">
                  <div>
                    <Label htmlFor="email" className="text-sm text-gray-600 mb-2 block">
                      Email Address
                    </Label>
                    <Input
                      id="email"
                      type="email"
                      className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Use the email address you gave your agent
                    </p>
                  </div>

                  <Button 
                    type="submit" 
                    className="w-full bg-gray-600 hover:bg-gray-700 text-white font-medium py-2.5 rounded"
                  >
                    SIGN IN
                  </Button>

                  <div className="relative my-6">
                    <div className="absolute inset-0 flex items-center">
                      <span className="w-full border-t border-gray-300" />
                    </div>
                    <div className="relative flex justify-center text-sm">
                      <span className="bg-white px-4 text-gray-500">or</span>
                    </div>
                  </div>

                  <Button 
                    type="button" 
                    variant="outline" 
                    className="w-full border border-gray-300 hover:bg-gray-50 text-gray-700 font-medium py-2.5 rounded flex items-center justify-center"
                  >
                    <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                      <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    Sign in with Google
                  </Button>

                  <p className="text-xs text-gray-500 text-center mt-4">
                    Make sure to use the email address you gave to your agent
                  </p>
                </form>
              </div>
            </div>

            {/* Footer Information */}
            <div className="text-center mt-8 space-y-1">
              <h3 className="font-semibold text-gray-700">Amandeep Singh Insurance Agency</h3>
              <p className="text-sm text-gray-600">Phone: 916-772-4006</p>
              <p className="text-sm text-gray-600">3017 Douglas Blvd, Suite 140 Roseville, CA 95661</p>
              <p className="text-xs text-gray-500 mt-3">
                © 2025 EZLynx. All rights reserved. 
                <a href="#" className="hover:underline ml-1 text-blue-600">Privacy Statement</a>
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ClientCenter;