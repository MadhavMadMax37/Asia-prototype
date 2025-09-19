import Header from "@/components/Header";

const PartnerAcelerate = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Partner Acelerate Program
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Join our exclusive partner acceleration program and grow your insurance business with comprehensive support and resources.
          </p>
        </div>

        {/* Program Benefits */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Advanced Training</h3>
            <p className="text-muted-foreground">
              Access comprehensive training modules and certification programs to enhance your expertise.
            </p>
          </div>
          
          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Marketing Support</h3>
            <p className="text-muted-foreground">
              Get professional marketing materials, digital assets, and campaign support to grow your client base.
            </p>
          </div>
          
          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Technology Tools</h3>
            <p className="text-muted-foreground">
              Access cutting-edge technology platforms and tools to streamline your operations and improve efficiency.
            </p>
          </div>
          
          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Commission Structure</h3>
            <p className="text-muted-foreground">
              Enjoy competitive commission rates with performance-based bonuses and incentives.
            </p>
          </div>
          
          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Dedicated Support</h3>
            <p className="text-muted-foreground">
              Work with a dedicated account manager who understands your business and goals.
            </p>
          </div>
          
          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Growth Opportunities</h3>
            <p className="text-muted-foreground">
              Access exclusive opportunities for business expansion and market development.
            </p>
          </div>
        </div>

        {/* Requirements Section */}
        <div className="bg-muted/30 p-8 rounded-lg mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-6 text-center">Program Requirements</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold text-foreground mb-4">Eligibility Criteria</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li>• Active insurance license in good standing</li>
                <li>• Minimum 2 years of insurance industry experience</li>
                <li>• Demonstrated sales performance record</li>
                <li>• Commitment to professional development</li>
                <li>• Technology proficiency and adaptability</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-foreground mb-4">Application Process</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li>• Complete online application form</li>
                <li>• Submit license documentation</li>
                <li>• Provide business references</li>
                <li>• Interview with program director</li>
                <li>• Background and compliance check</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Application Form */}
        <div className="bg-gradient-to-b from-purple-400 to-purple-300 p-8 rounded-lg">
          <div className="text-center text-white mb-8">
            <p className="text-lg mb-2">Interested in working together? Fill out</p>
            <p className="text-lg mb-2">some info and we will be in touch shortly!</p>
            <p className="text-lg font-semibold">We can't wait to hear from you!</p>
          </div>
          
          <div className="max-w-md mx-auto bg-white p-6 rounded border-4 border-blue-600">
            <form className="space-y-6">
              {/* Agent Name */}
              <div>
                <label className="block text-gray-800 font-semibold mb-2">
                  Agent Name <span className="text-sm text-gray-600">(required)</span>
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm text-gray-700 mb-1">First Name</label>
                    <input 
                      type="text" 
                      className="w-full p-3 border border-gray-300 rounded bg-purple-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-700 mb-1">Last Name</label>
                    <input 
                      type="text" 
                      className="w-full p-3 border border-gray-300 rounded bg-purple-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>
              </div>

              {/* Agent Email */}
              <div>
                <label className="block text-gray-800 font-semibold mb-2">
                  Agent Email <span className="text-sm text-gray-600">(required)</span>
                </label>
                <input 
                  type="email" 
                  className="w-full p-3 border border-gray-300 rounded bg-purple-50 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2"
                  required
                />
                <div className="flex items-center">
                  <input 
                    type="checkbox" 
                    id="newsletter" 
                    className="mr-2"
                  />
                  <label htmlFor="newsletter" className="text-sm text-gray-700">
                    Sign up for news and updates
                  </label>
                </div>
              </div>

              {/* NLG Agent Code */}
              <div>
                <label className="block text-gray-800 font-semibold mb-2">
                  NLG Agent Code <span className="text-sm text-gray-600">(required)</span>
                </label>
                <input 
                  type="text" 
                  className="w-full p-3 border border-gray-300 rounded bg-purple-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              {/* Phone */}
              <div>
                <label className="block text-gray-800 font-semibold mb-2">Phone</label>
                <input 
                  type="tel" 
                  className="w-full p-3 border border-gray-300 rounded bg-purple-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Submit Button */}
              <div>
                <button 
                  type="submit"
                  className="bg-blue-600 text-white font-semibold py-3 px-8 rounded hover:bg-blue-700 transition-colors duration-200"
                >
                  Submit
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Contact Information */}
        <div className="mt-12 text-center">
          <h3 className="text-2xl font-semibold text-foreground mb-4">Questions About the Program?</h3>
          <p className="text-muted-foreground mb-4">
            Contact our Partner Development team for more information
          </p>
          <div className="space-y-2">
            <p className="text-foreground font-medium">Email: partners@amandeepsinghagency.com</p>
            <p className="text-foreground font-medium">Phone: (555) 123-4567</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PartnerAcelerate;