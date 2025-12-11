import React, { useState } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';

// --- LEAFLET ICON FIX ---
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

// --- HELPER & UI COMPONENTS ---
const LeafIcon = ({ className = "h-10 w-10" }) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={`${className} text-green-400`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.898 20.562L16.25 22.5l-.648-1.938a3.375 3.375 0 00-2.658-2.658L11.25 18l1.938-.648a3.375 3.375 0 002.658-2.658L16.25 13l.648 1.938a3.375 3.375 0 002.658 2.658L21 18l-1.938.648a3.375 3.375 0 00-2.658 2.658z" />
    </svg>
);

const ResultCard = ({ title, data, error }) => {
    if (error) {
        return (
            <div className="mt-6 bg-red-900/50 border border-red-700 p-4 rounded-lg shadow-lg animate-fade-in">
                <h3 className="text-xl font-bold text-red-300 mb-2">Error</h3>
                <p className="text-red-200">{data.error || "An unknown error occurred."}</p>
            </div>
        );
    }
    return (
        <div className="mt-6 bg-gray-800 p-6 rounded-lg shadow-lg animate-fade-in">
            <h3 className="text-xl font-bold text-green-400 mb-4">{title}</h3>
            <div className="space-y-2 text-gray-300">
                {Object.entries(data).map(([key, value]) => (
                    <div key={key} className="flex justify-between border-b border-gray-700 py-2">
                        <span className="font-semibold capitalize">{key.replace(/_/g, ' ')}:</span>
                        <span className="text-right font-mono">{typeof value === 'object' ? JSON.stringify(value) : value}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

const MapClickHandler = ({ onMapClick }) => {
  useMapEvents({ click(e) { onMapClick(e.latlng); } });
  return null;
};

// --- LOGIN PAGE ---
function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [registerData, setRegisterData] = useState({
    username: '',
    password: '',
    email: ''
  });
  const [registerMessage, setRegisterMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/login/', { username, password });
      onLoginSuccess(response.data.user.username);
    } catch (err) {
      setError('Invalid username or password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setRegisterMessage('');
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/register/', registerData);
      setRegisterMessage('Registration successful! You can now login.');
      setRegisterData({ username: '', password: '', email: '' });
      setTimeout(() => {
        setShowRegister(false);
        setRegisterMessage('');
      }, 3000);
    } catch (error) {
      setRegisterMessage(error.response?.data?.error || 'Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      {/* Registration Modal */}
      {showRegister && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-2xl p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold text-white mb-6 text-center">Create Account</h2>
            
            <form onSubmit={handleRegister} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Username</label>
                <input
                  type="text"
                  value={registerData.username}
                  onChange={(e) => setRegisterData({...registerData, username: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:outline-none"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
                <input
                  type="email"
                  value={registerData.email}
                  onChange={(e) => setRegisterData({...registerData, email: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:outline-none"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
                <input
                  type="password"
                  value={registerData.password}
                  onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:outline-none"
                  required
                />
              </div>
              
              <button
                type="submit"
                className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition-colors"
              >
                Register
              </button>
              
              <button
                type="button"
                onClick={() => setShowRegister(false)}
                className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition-colors"
              >
                Cancel
              </button>
            </form>
            
            {registerMessage && (
              <div className={`mt-4 p-3 rounded text-center ${
                registerMessage.includes('successful') ? 'bg-green-900 text-green-200' : 'bg-red-900 text-red-200'
              }`}>
                {registerMessage}
              </div>
            )}
          </div>
        </div>
      )}

      <div className="w-full max-w-4xl rounded-lg shadow-2xl overflow-hidden bg-gray-800 md:flex">
        <div className="w-full md:w-1/2 p-8 md:p-12">
          <div className="flex flex-col items-center md:items-start">
            <div className="text-center md:text-left mb-8">
               <div className="flex items-center justify-center md:justify-start space-x-3 mb-4">
                  <LeafIcon className="h-12 w-12" />
                  <h1 className="text-3xl font-bold text-white">Krishi Sakhi</h1>
               </div>
              <h4 className="mt-1 mb-5 pb-1 text-xl font-light text-gray-300">Welcome to your AI Farming Assistant</h4>
            </div>
            <p className="text-gray-400 mb-4">Please login to your account</p>
            <form onSubmit={handleSubmit} className="w-full">
              <input placeholder='Username' type='text' value={username} onChange={(e) => setUsername(e.target.value)} className="w-full bg-gray-700 border border-gray-600 rounded-md p-3 text-white focus:ring-2 focus:ring-green-500 focus:outline-none mb-4" />
              <input placeholder='Password' type='password' value={password} onChange={(e) => setPassword(e.target.value)} className="w-full bg-gray-700 border border-gray-600 rounded-md p-3 text-white focus:ring-2 focus:ring-green-500 focus:outline-none mb-4" />
              {error && <p className="text-red-400 text-sm mb-4 text-center">{error}</p>}
              <div className="text-center pt-1 mb-5 pb-1">
                <button disabled={isLoading} className="mb-4 w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-md transition-colors duration-300 disabled:bg-gray-500">{isLoading ? 'Signing in...' : 'Sign in'}</button>
                <a className="text-gray-500 hover:text-green-400" href="#!">Forgot password?</a>
              </div>
              <div className="flex items-center justify-center">
                <p className="mb-0 text-gray-400">Don't have an account?</p>
                <button 
                  type="button" 
                  className='mx-2 text-green-400 hover:text-green-300 font-semibold'
                  onClick={() => setShowRegister(true)}
                >
                  Register
                </button>
              </div>
            </form>
          </div>
        </div>
        <div className="hidden md:flex w-1/2 items-center justify-center bg-green-800/50 p-12 text-white text-center rounded-r-lg" style={{ background: 'linear-gradient(to right, #166534, #15803d, #16a34a)' }}>
          <div>
            <h4 className="text-3xl font-bold mb-4">More than just an App</h4>
            <p className="text-lg leading-relaxed">Krishi Sakhi is your data-driven partner. We combine AI with real-time data to help you make smarter decisions, increase your yield, and build a sustainable future.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// --- MAIN DASHBOARD ---
function Dashboard({ username }) {
    const [activeTab, setActiveTab] = useState('recommender');
    const [markerPosition, setMarkerPosition] = useState(null);
    const [recommenderResult, setRecommenderResult] = useState(null);
    const [isLoadingRecommender, setIsLoadingRecommender] = useState(false);
    const [doctorImage, setDoctorImage] = useState(null);
    const [doctorResult, setDoctorResult] = useState(null);
    const [isLoadingDoctor, setIsLoadingDoctor] = useState(false);
    const [previewImage, setPreviewImage] = useState(null);
    const [assistantInput, setAssistantInput] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [isLoadingAssistant, setIsLoadingAssistant] = useState(false);

    const handleMapClick = async (latlng) => {
        setMarkerPosition(latlng);
        setIsLoadingRecommender(true);
        setRecommenderResult(null);
        
        // Fix: Round coordinates to 6 decimal places
        const latitude = parseFloat(latlng.lat.toFixed(6));
        const longitude = parseFloat(latlng.lng.toFixed(6));
        
        console.log('Sending coordinates:', { latitude, longitude });
        
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/recommend-from-location/', { 
                latitude: latitude,
                longitude: longitude
            }, {
                headers: {
                    'Content-Type': 'application/json',
                },
                timeout: 10000 // 10 second timeout
            });
            
            console.log('API Response:', response.data);
            setRecommenderResult({ data: response.data });
            
        } catch (error) {
            console.error('API Error:', error);
            let errorMessage = "Failed to get recommendation. ";
            
            if (error.response) {
                // Server responded with error status
                errorMessage += `Server error: ${error.response.status} - ${JSON.stringify(error.response.data)}`;
            } else if (error.request) {
                // Request made but no response received
                errorMessage += "Backend server is not responding. Please check if the server is running.";
            } else {
                // Something else happened
                errorMessage += error.message;
            }
            
            setRecommenderResult({ 
                error: true, 
                data: { error: errorMessage } 
            });
        } finally {
            setIsLoadingRecommender(false);
        }
    };
    
    const handleDoctorImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setDoctorImage(file);
            setPreviewImage(URL.createObjectURL(file));
            setDoctorResult(null);
        }
    };

    const handleDoctorSubmit = async (e) => {
        e.preventDefault();
        if (!doctorImage) return;
        setIsLoadingDoctor(true);
        setDoctorResult(null);
        const formData = new FormData();
        formData.append('image', doctorImage);
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/predict-disease-v2/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
            setDoctorResult({ data: response.data });
        } catch (error) {
            setDoctorResult({ error: true, data: { error: "Failed to get prediction. Is the backend server running?" }});
        } finally {
            setIsLoadingDoctor(false);
        }
    };

    const handleAssistantSubmit = async (e) => {
        e.preventDefault();
        if (!assistantInput.trim()) return;
        const newChatHistory = [...chatHistory, { role: 'user', text: assistantInput }];
        setChatHistory(newChatHistory);
        setAssistantInput('');
        setIsLoadingAssistant(true);
        
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/assistant/', { message: assistantInput });
            setChatHistory([...newChatHistory, { role: 'model', text: response.data.response }]);
        } catch (error) {
            setChatHistory([...newChatHistory, { role: 'model', text: "Sorry, I'm having trouble connecting to my knowledge base. Please try again." }]);
        } finally {
            setIsLoadingAssistant(false);
        }
    };

    const renderContent = () => {
        switch (activeTab) {
        case 'recommender': return (
            <div className="animate-fade-in">
                <h2 className="text-2xl font-bold text-white mb-4">"Magic Map" Crop Recommender</h2>
                <p className="text-gray-400 mb-6">Click anywhere on the map of Karnataka to get an instant, AI-powered crop recommendation for that location.</p>
                <div className="h-96 w-full rounded-lg overflow-hidden border-2 border-green-500/50" id="map">
                    <MapContainer center={[15.3173, 75.7139]} zoom={7} style={{ height: '100%', width: '100%' }} className="h-full w-full">
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'/>
                        <MapClickHandler onMapClick={handleMapClick} />
                        {markerPosition && <Marker position={markerPosition}></Marker>}
                    </MapContainer>
                </div>
                {isLoadingRecommender && <div className="text-center mt-4 text-green-300">Analyzing location...</div>}
                {recommenderResult && <ResultCard title="Recommendation Result" {...recommenderResult} />}
            </div>
        );
        case 'doctor': return (
            <div className="animate-fade-in">
                <h2 className="text-2xl font-bold text-white mb-4">Multi-Crop Doctor (V2.0)</h2>
                <p className="text-gray-400 mb-6">Upload a clear photo of a Tomato, Potato, or Maize leaf to diagnose diseases.</p>
                <form onSubmit={handleDoctorSubmit}>
                    <div className="flex flex-col items-center bg-gray-700 border-2 border-dashed border-gray-500 rounded-lg p-8">
                        <input type="file" id="imageUpload" accept="image/*" onChange={handleDoctorImageChange} className="hidden" />
                        <label htmlFor="imageUpload" className="cursor-pointer bg-gray-600 text-white font-bold py-2 px-4 rounded-md hover:bg-gray-500 transition-colors">Choose an Image</label>
                        {previewImage && <img src={previewImage} alt="Preview" className="mt-4 rounded-lg max-h-48" />}
                    </div>
                    <button type="submit" disabled={!doctorImage || isLoadingDoctor} className="mt-4 w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-md transition-colors duration-300 disabled:bg-gray-500">{isLoadingDoctor ? 'Diagnosing...' : 'Diagnose Plant'}</button>
                </form>
                {doctorResult && <ResultCard title="Diagnosis Result" {...doctorResult} />}
            </div>
        );
        case 'assistant': return (
            <div className="animate-fade-in">
                <h2 className="text-2xl font-bold text-white mb-4">AI Assistant (for Karnataka)</h2>
                <p className="text-gray-400 mb-6">Ask me any question about farming, crops, or schemes in Karnataka.</p>
                <div className="bg-gray-900/50 rounded-lg h-96 overflow-y-auto p-4 flex flex-col space-y-4">
                    {chatHistory.map((msg, index) => (
                        <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-xs md:max-w-md p-3 rounded-lg ${msg.role === 'user' ? 'bg-green-600 text-white' : 'bg-gray-700 text-gray-200'}`}>{msg.text}</div>
                        </div>
                    ))}
                    {isLoadingAssistant && <div className="self-start"><div className="p-3 rounded-lg bg-gray-700 text-gray-200">Thinking...</div></div>}
                </div>
                <form onSubmit={handleAssistantSubmit} className="mt-4 flex space-x-2">
                    <input type="text" value={assistantInput} onChange={(e) => setAssistantInput(e.target.value)} placeholder="Ask your question here..." className="flex-grow bg-gray-700 border border-gray-600 rounded-md p-2 text-white focus:ring-2 focus:ring-green-500 focus:outline-none"/>
                    <button type="submit" disabled={isLoadingAssistant} className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-md transition-colors duration-300 disabled:bg-gray-500">Send</button>
                </form>
            </div>
        );
        default: return null;
        }
    };

    return (
        <div className="bg-gray-900 min-h-screen text-white font-sans p-4 sm:p-8">
            <div className="max-w-4xl mx-auto">
                <header className="flex items-center justify-between pb-8 border-b border-gray-700">
                    <div className="flex items-center space-x-4">
                        <LeafIcon />
                        <div>
                            <h1 className="text-3xl font-bold text-white">Krishi Sakhi</h1>
                            <span className="text-green-400">V2.0 / Welcome, {username}!</span>
                        </div>
                    </div>
                    <button onClick={() => window.location.reload()} className="text-gray-400 hover:text-white transition-colors">Logout</button>
                </header>
                <nav className="my-8 flex justify-center space-x-1 sm:space-x-2 bg-gray-800 p-2 rounded-lg">
                    <button onClick={() => setActiveTab('recommender')} className={`w-1/3 px-2 py-2 rounded-md font-semibold text-sm sm:text-base transition-colors ${activeTab === 'recommender' ? 'bg-green-600' : 'hover:bg-gray-700'}`}>Magic Map</button>
                    <button onClick={() => setActiveTab('doctor')} className={`w-1/3 px-2 py-2 rounded-md font-semibold text-sm sm:text-base transition-colors ${activeTab === 'doctor' ? 'bg-green-600' : 'hover:bg-gray-700'}`}>Crop Doctor</button>
                    <button onClick={() => setActiveTab('assistant')} className={`w-1/3 px-2 py-2 rounded-md font-semibold text-sm sm:text-base transition-colors ${activeTab === 'assistant' ? 'bg-green-600' : 'hover:bg-gray-700'}`}>AI Assistant</button>
                </nav>
                <main className="bg-gray-800/50 p-6 sm:p-8 rounded-xl shadow-2xl">
                    {renderContent()}
                </main>
                <footer className="text-center mt-8 text-gray-500 text-sm">&copy; 2025 Krishi Sakhi. Built with AI, for farmers.</footer>
            </div>
        </div>
    );
}

// --- APP WRAPPER ---
function App() {
  const [user, setUser] = useState(null);

  const handleLoginSuccess = (username) => {
    setUser(username);
  };

  if (user) {
    return <Dashboard username={user} />;
  } else {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }
}

export default App;