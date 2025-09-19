import Header from "@/components/Header";
import { Link } from "react-router-dom";

const AcelerateReferral = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="flex items-center justify-center min-h-[calc(100vh-120px)]">
        <div className="bg-gradient-to-b from-purple-400 to-blue-400 p-12 rounded-lg text-center max-w-2xl mx-4">
          <div className="text-white space-y-4 mb-8">
            <p className="text-xl font-medium">
              Interested in working together? Fill out
            </p>
            <p className="text-xl font-medium">
              some info and we will be in touch shortly!
            </p>
            <p className="text-xl font-semibold">
              We can't wait to hear from you!
            </p>
          </div>
          
          <Link 
            to="/get-a-quote"
            className="bg-black text-white px-8 py-3 rounded-full font-semibold text-lg hover:bg-gray-800 transition-colors duration-200 inline-block"
          >
            Fill the Form
          </Link>
        </div>
      </main>
    </div>
  );
};

export default AcelerateReferral;