import  Form from './Form'

import appStyles from './app.module.css';

function App() {
  return (
    <div className={appStyles.wrapper}>
      <div className={appStyles.content}>
        <Form />
      </div>
    </div>
  );
}

export default App;
