import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { X } from "lucide-react";

interface QuoteModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const QuoteModal = ({ open, onOpenChange }: QuoteModalProps) => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    country: "United States",
    addressLine1: "",
    addressLine2: "",
    city: "",
    state: "",
    zipCode: "",
    phoneNumber: "",
    email: "",
    personalLines: false,
    commercialLines: false,
    lifeAndHealth: false,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      // Convert form data to match backend schema
      const leadData = {
        firstName: formData.firstName,
        lastName: formData.lastName,
        email: formData.email,
        phoneNumber: formData.phoneNumber,
        country: formData.country,
        addressLine1: formData.addressLine1,
        addressLine2: formData.addressLine2 || "",
        city: formData.city,
        state: formData.state,
        zipCode: formData.zipCode,
        personalLines: formData.personalLines,
        commercialLines: formData.commercialLines,
        lifeAndHealth: formData.lifeAndHealth,
        source: "website"
      };

      // Submit to CRM API
      const response = await fetch('/api/leads/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(leadData)
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Lead created successfully:', result);
        
        // Show success message (you can replace this with a toast notification)
        alert('Thank you! Your quote request has been submitted successfully. We will contact you within 24 hours.');
        
        // Reset form
        setFormData({
          firstName: "",
          lastName: "",
          country: "United States",
          addressLine1: "",
          addressLine2: "",
          city: "",
          state: "",
          zipCode: "",
          phoneNumber: "",
          email: "",
          personalLines: false,
          commercialLines: false,
          lifeAndHealth: false,
        });
        
        onOpenChange(false);
      } else {
        const errorData = await response.json();
        console.error('Error submitting lead:', errorData);
        alert('There was an error submitting your request. Please try again or call us directly at 916-772-4006.');
      }
    } catch (error) {
      console.error('Network error:', error);
      alert('There was an error submitting your request. Please check your internet connection and try again.');
    }
  };

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md max-h-[90vh] overflow-y-auto p-6 bg-gray-200">
        <DialogHeader className="relative">
          <DialogTitle className="text-blue-600 text-xl font-bold text-left">
            Get A Quote
          </DialogTitle>
          <Button
            variant="ghost"
            size="icon"
            className="absolute -top-2 -right-2 h-6 w-6"
            onClick={() => onOpenChange(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Name Section */}
          <div>
            <Label className="text-blue-600 font-bold text-base">
              Name <span className="text-blue-600">(required)</span>
            </Label>
            <div className="grid grid-cols-2 gap-3 mt-2">
              <div>
                <Label htmlFor="firstName" className="text-sm text-gray-700">First Name</Label>
                <Input
                  id="firstName"
                  value={formData.firstName}
                  onChange={(e) => handleInputChange("firstName", e.target.value)}
                  className="mt-1 bg-white border-gray-400"
                  required
                />
              </div>
              <div>
                <Label htmlFor="lastName" className="text-sm text-gray-700">Last Name</Label>
                <Input
                  id="lastName"
                  value={formData.lastName}
                  onChange={(e) => handleInputChange("lastName", e.target.value)}
                  className="mt-1 bg-white border-gray-400"
                  required
                />
              </div>
            </div>
          </div>

          {/* Address Section */}
          <div>
            <Label className="text-blue-600 font-bold text-base">
              Address <span className="text-blue-600">(required)</span>
            </Label>
            
            <div className="mt-2 space-y-3">
              <div>
                <Label htmlFor="country" className="text-sm text-gray-700">Country</Label>
                <Select value={formData.country} onValueChange={(value) => handleInputChange("country", value)}>
                  <SelectTrigger className="mt-1 bg-white border-gray-400">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="United States">United States</SelectItem>
                    <SelectItem value="Canada">Canada</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="addressLine1" className="text-sm text-gray-700">
                  Address Line 1 <span className="text-blue-600">(required)</span>
                </Label>
                <Input
                  id="addressLine1"
                  value={formData.addressLine1}
                  onChange={(e) => handleInputChange("addressLine1", e.target.value)}
                  className="mt-1 bg-white border-gray-400"
                  required
                />
              </div>

              <div>
                <Label htmlFor="addressLine2" className="text-sm text-gray-700">Address Line 2</Label>
                <Input
                  id="addressLine2"
                  value={formData.addressLine2}
                  onChange={(e) => handleInputChange("addressLine2", e.target.value)}
                  className="mt-1 bg-white border-gray-400"
                />
              </div>

              <div className="grid grid-cols-3 gap-2">
                <div>
                  <Label htmlFor="city" className="text-sm text-gray-700">
                    City <span className="text-blue-600">(required)</span>
                  </Label>
                  <Input
                    id="city"
                    value={formData.city}
                    onChange={(e) => handleInputChange("city", e.target.value)}
                    className="mt-1 bg-white border-gray-400"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="state" className="text-sm text-gray-700">
                    State <span className="text-blue-600">(required)</span>
                  </Label>
                  <Input
                    id="state"
                    value={formData.state}
                    onChange={(e) => handleInputChange("state", e.target.value)}
                    className="mt-1 bg-white border-gray-400"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="zipCode" className="text-sm text-gray-700">
                    ZIP Code <span className="text-blue-600">(required)</span>
                  </Label>
                  <Input
                    id="zipCode"
                    value={formData.zipCode}
                    onChange={(e) => handleInputChange("zipCode", e.target.value)}
                    className="mt-1 bg-white border-gray-400"
                    required
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Phone Number */}
          <div>
            <Label htmlFor="phoneNumber" className="text-blue-600 font-bold text-base">
              Phone Number <span className="text-blue-600">(required)</span>
            </Label>
            <Input
              id="phoneNumber"
              value={formData.phoneNumber}
              onChange={(e) => handleInputChange("phoneNumber", e.target.value)}
              className="mt-2 bg-white border-gray-400"
              required
            />
          </div>

          {/* Email */}
          <div>
            <Label htmlFor="email" className="text-blue-600 font-bold text-base">
              Email <span className="text-blue-600">(required)</span>
            </Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => handleInputChange("email", e.target.value)}
              className="mt-2 bg-white border-gray-400"
              required
            />
          </div>

          {/* Line of Business */}
          <div>
            <Label className="text-blue-600 font-bold text-base">
              Line of Business <span className="text-blue-600">(required)</span>
            </Label>
            <div className="mt-2 space-y-3">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="personalLines"
                  checked={formData.personalLines}
                  onCheckedChange={(checked) => handleInputChange("personalLines", checked as boolean)}
                />
                <Label htmlFor="personalLines" className="text-sm text-blue-600">
                  Personal Lines (auto, home, umbrella, motorcycle etc)
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="commercialLines"
                  checked={formData.commercialLines}
                  onCheckedChange={(checked) => handleInputChange("commercialLines", checked as boolean)}
                />
                <Label htmlFor="commercialLines" className="text-sm text-blue-600">
                  Commercial Lines
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="lifeAndHealth"
                  checked={formData.lifeAndHealth}
                  onCheckedChange={(checked) => handleInputChange("lifeAndHealth", checked as boolean)}
                />
                <Label htmlFor="lifeAndHealth" className="text-sm text-blue-600">
                  Life and Health
                </Label>
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-center pt-4">
            <Button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-2 rounded"
            >
              Send
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default QuoteModal;