import "./Register.css";

export default function Register() {
  return (
    <main className="register-page">
      <section className="register-card" aria-labelledby="register-title">
        <a className="register-brand" href="/" aria-label="Project home">
          <span className="register-brand-mark" aria-hidden="true">
            D
          </span>
          <span>My Data Science Project</span>
        </a>

        <div className="register-heading">
          <p className="register-eyebrow">CREATE YOUR ACCOUNT</p>
          <h1 id="register-title">Sign up</h1>
          <p>Join us and start exploring the project.</p>
        </div>

        <form className="register-form">
          <div className="register-name-row">
            <label>
              First Name
              <input
                type="text"
                name="firstName"
                autoComplete="given-name"
                placeholder="First name"
                required
              />
            </label>
            <label>
              Last Name
              <input
                type="text"
                name="lastName"
                autoComplete="family-name"
                placeholder="Last name"
                required
              />
            </label>
          </div>

          <label>
            Username
            <input
              type="text"
              name="username"
              autoComplete="username"
              placeholder="Choose a username"
              required
            />
          </label>

          <label>
            Email
            <input
              type="email"
              name="email"
              autoComplete="email"
              placeholder="you@example.com"
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              name="password"
              autoComplete="new-password"
              placeholder="Create a password"
              minLength={8}
              required
            />
          </label>

          <button type="submit">Register</button>
        </form>

        <p className="register-login">
          Already have an account? <a href="/login">Log in</a>
        </p>
      </section>
    </main>
  );
}
