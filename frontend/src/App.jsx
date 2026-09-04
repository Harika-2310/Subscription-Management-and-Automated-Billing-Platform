import { useEffect, useState } from "react";
import axios from "axios";
import "./index.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState({
    mrr: 0,
    churn_rate: 0,
    trial_conversion: 0,
    failed_payments: 0,
  });

  const [taxReport, setTaxReport] = useState([]);
  const [failedPayments, setFailedPayments] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true);
        setError("");

        const [
          summaryResponse,
          taxResponse,
          failedResponse,
        ] = await Promise.all([
          axios.get(`${API}/dashboard/summary`),
          axios.get(`${API}/invoices/tax-report`),
          axios.get(`${API}/dashboard/failed-payments`),
        ]);

        setSummary(summaryResponse.data);
        setTaxReport(taxResponse.data);
        setFailedPayments(failedResponse.data);
      } catch (err) {
        console.error("Dashboard error:", err);
        setError(
          "Unable to load dashboard data. Please check that the backend is running."
        );
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">
          Loading dashboard...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="error">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="header">
        <h1>Subscription Billing Dashboard</h1>
        <p>Admin Dashboard</p>
      </header>

      <section className="cards">
        <div className="card">
          <h3>MRR</h3>
          <p>₹{summary.mrr}</p>
        </div>

        <div className="card">
          <h3>Churn Rate</h3>
          <p>{summary.churn_rate}%</p>
        </div>

        <div className="card">
          <h3>Trial Conversion</h3>
          <p>{summary.trial_conversion}%</p>
        </div>

        <div className="card">
          <h3>Failed Payments</h3>
          <p>{summary.failed_payments}</p>
        </div>
      </section>

      <section className="panel">
        <h2>Tax Report</h2>

        {taxReport.length === 0 ? (
          <p>No tax records found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Country</th>
                <th>Region</th>
                <th>Total Tax</th>
              </tr>
            </thead>

            <tbody>
              {taxReport.map((item, index) => (
                <tr key={index}>
                  <td>{item.country}</td>
                  <td>{item.region || "-"}</td>
                  <td>₹{item.total_tax}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section className="panel">
        <h2>Failed Payments</h2>

        {failedPayments.length === 0 ? (
          <p>No failed payments.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Payment ID</th>
                  <th>Invoice ID</th>
                  <th>Amount</th>
                  <th>Payment Method</th>
                  <th>Retry Count</th>
                  <th>Next Retry</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {failedPayments.map((payment) => (
                  <tr key={payment.id}>
                    <td>{payment.id}</td>
                    <td>{payment.invoice_id}</td>
                    <td>₹{payment.amount}</td>
                    <td>{payment.payment_method || "-"}</td>
                    <td>{payment.retry_count}</td>
                    <td>
                      {payment.next_retry_at
                        ? new Date(
                            payment.next_retry_at
                          ).toLocaleString()
                        : "-"}
                    </td>
                    <td>{payment.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;