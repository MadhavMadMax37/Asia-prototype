import Header from "@/components/Header";

const Careers = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="py-16">
        <div className="container mx-auto px-4">
          {/* Title */}
          <div className="text-center mb-12">
            <h1 className="text-3xl lg:text-4xl font-bold text-blue-600 uppercase">
              LOOKING FOR A NEW CAREER?
            </h1>
          </div>

          {/* Job Sections */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12 max-w-6xl mx-auto">
            
            {/* Customer Service Representative */}
            <div className="space-y-6">
              <div className="bg-gray-100 p-4 text-center">
                <h2 className="text-lg font-bold text-gray-800 uppercase tracking-wide">
                  CUSTOMER SERVICE REPRESENTATIVE
                </h2>
              </div>
              
              <div className="space-y-4 text-gray-700 leading-relaxed">
                <p>
                  We are looking to hire a motivated individual who is willing to learn or have 
                  previous experience working in the insurance industry. Our customer service rep 
                  will be responsible for overall client experience as well as maintain client 
                  and agency relationships.
                </p>
              </div>
            </div>

            {/* Skills Needed */}
            <div className="space-y-6 lg:border-l lg:border-r lg:border-gray-300 lg:px-8">
              <div className="bg-gray-100 p-4 text-center">
                <h2 className="text-lg font-bold text-gray-800 uppercase tracking-wide">
                  SKILLS NEEDED
                </h2>
              </div>
              
              <div className="space-y-4 text-gray-700 leading-relaxed">
                <p className="font-bold text-center">
                  **BILINGUAL PUNJABI SPEAKING A MUST.**
                </p>
                
                <div className="space-y-3">
                  <p>P&C license a plus but not a requirement (we will help you to obtain your license)</p>
                  <p>Must have Microsoft Office experience</p>
                  <p>Must have excellent communication skills and an ability to multitask and stay organized.</p>
                  <p>Looking for a highly driven motivated individual to grow with the agency.</p>
                  <p>Previous customer service experience a plus, but not required.</p>
                  <p>Be professional with a positive attitude and motivation to grow!</p>
                </div>
              </div>
            </div>

            {/* Duties */}
            <div className="space-y-6">
              <div className="bg-gray-100 p-4 text-center">
                <h2 className="text-lg font-bold text-gray-800 uppercase tracking-wide">
                  DUTIES
                </h2>
              </div>
              
              <div className="space-y-4 text-gray-700 leading-relaxed">
                <div className="space-y-3">
                  <p>Must consistently and efficiently follow up with clients requests and carrier requirements.</p>
                  <p>Handle all inbound and outbound agency calls.</p>
                  <p>Work the CMS system and stay up to date on all clients profiles.</p>
                  <p>Open the door for cross selling opportunities within our book of business.</p>
                  <p>Process renewals.</p>
                  <p>Some light marketing involved as well.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div className="text-center mt-16">
            <div className="border-t border-gray-300 pt-8 max-w-4xl mx-auto">
              <p className="text-lg text-gray-700">
                Interested? Please send us a resume to{' '}
                <a 
                  href="mailto:TEAM@ASIAINC.CO" 
                  className="text-blue-600 hover:text-blue-800 font-semibold"
                >
                  TEAM@ASIAINC.CO
                </a>
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Careers;