import React from "react";
import Footer from "../components/Footer";
import "./css/bootstrap.min.css";
import "./css/animate.css";
import "./css/themify-icons.css";
import "./css/magnific-popup.css";
import "./css/nice-select.css";
import "./css/slick.css";
import "./css/style.css";
import bannerImage from "./img/banner_img.png";
import topservice from "./img/top_service.png";

export default function Home() {
  return (
    <div>
      <header className="main_menu home_menu">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12">
              <nav className="navbar navbar-expand-lg navbar-light">
                <lord-icon
                  src="https://cdn.lordicon.com/hpcxqbph.json"
                  trigger="loop"
                  style={{ width: "80px", height: "80px" }}
                ></lord-icon>
                <a className="navbar-brand" style={{ fontWeight: "bold" }}>
                  OCRxAI
                </a>

                <button
                  className="navbar-toggler"
                  type="button"
                  data-toggle="collapse"
                  data-target="#navbarSupportedContent"
                  aria-controls="navbarSupportedContent"
                  aria-expanded="false"
                  aria-label="Toggle navigation"
                >
                  <span className="navbar-toggler-icon"></span>
                </button>
                <div
                  className="collapse navbar-collapse main-menu-item justify-content-center"
                  id="navbarSupportedContent"
                >
                  <ul className="navbar-nav align-items-center">
                    {/* Add navigation links here if needed */}
                  </ul>
                </div>
                <a className="btn_2 d-none d-lg-block" href="/login">
                  LOGIN
                </a>
              </nav>
            </div>
          </div>
        </div>
      </header>
      <section className="banner_part">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-5 col-xl-5">
              <div className="banner_text">
                <div className="banner_text_iner">
                  <h5>Cracking Doctor Codes!</h5>
                  <h1>OCRxAI</h1>
                  <p>
                    OCRxAI automates the extraction of medical diagnoses from
                    handwritten medical forms, enhancing efficiency and accuracy
                    in healthcare claims processing. Our solution leverages
                    state-of-the-art OCR technology to accurately recognize and
                    extract handwritten text, including complex medical
                    diagnoses. Extracted diagnoses are compiled into an Excel
                    file, streamlining integration into existing healthcare
                    systems.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-lg-7">
              <div className="banner_img">
                <img src={bannerImage} alt="Banner" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Us Section */}
      <section className="about_us padding_top">
        <div className="container">
          <div className="row justify-content-between align-items-center mb-5">
            <div className="col-md-6 col-lg-6">
              <div className="about_us_img">
                <img src={topservice} alt="About Us" />
              </div>
            </div>
            <div className="col-md-6 col-lg-6">
              <div className="about_us_text">
                <h2>About Us</h2>
                <p>
                  We are Team Deep Pixelated, a group of tech enthusiasts united
                  by our passion for innovation. Comprising Avi Gupta, Kartikey
                  Bhatnagar, and Vaishali Singh, we met during a college club
                  event and quickly bonded over our shared interest in
                  technology and solving real-world problems. With OCRxAI, we're
                  excited to innovate in the healthcare sector, aiming to
                  digitize and enhance medical processes.
                </p>
                <div className="banner_item">
                  <div className="single_item">
                    <h5>High-Precision Extraction</h5>
                  </div>
                  <div className="single_item">
                    <h5>Automated ROI Detection</h5>
                  </div>
                  <div className="single_item">
                    <h5>Seamless Data Compilation</h5>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}

