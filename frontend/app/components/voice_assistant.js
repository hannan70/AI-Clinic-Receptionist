"use client"
export default function VoiceAssistant(){
    return(
    <div className="agent_section mt-5">
      <div className="container">
        <div className="agent_area">
          <div className="row">
            <div className="col-md-8">
                <div className="card shadow">
                  <div className="card-header bg-primary text-white">
                    <h4>AI Clinic Receptionist</h4>
                  </div>  
                  <div className="conversation_list"> 
                    <div className="conversation_list_area">
                        <div className="conversation_item">
                            <div className="u">
                                <p>You</p>
                                <h5>What are your opening hours?</h5>
                            </div>
                            <div className="ai">
                                <p>AI Receptionist</p>
                                <h5>We are open Monday to Friday from 9 AM to 7 PM.</h5>
                            </div>
                        </div>
                        <div className="conversation_item">
                            <div className="u">
                                <p>You</p>
                                <h5>What are your opening hours?</h5>
                            </div>
                            <div className="ai">
                                <p>AI Receptionist</p>
                                <h5>We are open Monday to Friday from 9 AM to 7 PM.</h5>
                            </div>
                        </div>
                        <div className="conversation_item">
                            <div className="u">
                                <p>You</p>
                                <h5>What are your opening hours?</h5>
                            </div>
                            <div className="ai">
                                <p>AI Receptionist</p>
                                <h5>We are open Monday to Friday from 9 AM to 7 PM.</h5>
                            </div>
                        </div>
                        <div className="conversation_item">
                            <div className="u">
                                <p>You</p>
                                <h5>What are your opening hours?</h5>
                            </div>
                            <div className="ai">
                                <p>AI Receptionist</p>
                                <h5>We are open Monday to Friday from 9 AM to 7 PM.</h5>
                            </div>
                        </div>
                        <div className="conversation_item">
                            <div className="u">
                                <p>You</p>
                                <h5>What are your opening hours?</h5>
                            </div>
                            <div className="ai">
                                <p>AI Receptionist</p>
                                <h5>We are open Monday to Friday from 9 AM to 7 PM.</h5>
                            </div>
                        </div>
                    </div>
                  </div>
                </div>
            </div>
            <div className="col-md-4">
                <div className="card shadow p-3">
                    <div className="card-body text-center">
                        <h5 className="card-title">
                        Voice Assistant
                        </h5>
                        <p className="card-text">
                        Ready to assist patients
                        </p>
                        <p className="badge bg-secondary"> Disconnected</p>
                        <br></br>
                        <button className="btn btn-success">
                        Start Conversation
                        </button>
                    </div>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    )
}