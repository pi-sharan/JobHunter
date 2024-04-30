// import React from 'react';
// import './styles.css';

// const Footer = ({ teamMembers }) => {
//     console.log(teamMembers[0]);
//   return (
//     <footer className="footer">
//       <div className="footer-content">
//         <img src="../logo.svg" alt="JobHunter Logo" style={{ width: '50px', marginRight: '1rem' }} />
//         <h1>JobHunter</h1>
//         <div className="footer-team">
//           <p>Team Members:</p>
//           <table>
//             <tbody>
//               {teamMembers.map((member, index) => (
//                 <tr key={index}>
//                   <td>{member}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       </div>
//     </footer>
//   );
// };

// export default Footer;

import React from 'react';
import './styles.css';
import { useNavigate } from 'react-router-dom';

const Footer = ({ teamMembers }) => {
  const navigate = useNavigate();
  
  const handleOnclick = () => {
    navigate('/');
  }
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-logo-name">
            <img src={require('./logo.png')} alt="JobHunter Logo" style={{ width: '80px', marginRight: '1rem' }} onClick={handleOnclick}/>
            <h1>JobHunter</h1>
        </div>
        <div className="footer-team">
          <h3>Team Members:</h3>
          <table>
            <tbody>
              {teamMembers.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((member, index) => (
                    <td key={index}>{member}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
