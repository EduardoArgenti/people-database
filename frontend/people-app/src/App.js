import React, {useState, useEffect} from 'react'
import api from './api'

const App = () => {
    const [people, setPeople] = useState([]);
    const [formData, setFormData] = useState({
        name: '',
        birthdate: '',
        gender: '',
        nationality: ''
    });

    const fetchPeople = async () => {
        const response = await api.get('/people/');
        setPeople(response.data)
    };

    useEffect(() => {
        fetchPeople();
    }, []);

    const handleInputChange = (event) => {
        const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
        setFormData({
            ...formData,
            [event.target.name]: value
        });
    };

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        await api.post('/people/', formData);
        fetchPeople();
        setFormData({
            name: '',
            birthdate: '',
            gender: '',
            nationality: ''
        });
    };

    return (
        <div>
            <nav className='navbar navbar-dark bg-primary'>
                <div className='container-fluid'>
                    <a className='navbar-brand' href='#'>
                        People Database
                    </a>
                </div>
            </nav>

            <div className='container'>
                <form onSubmit={handleFormSubmit}>

                    <div className="mb-3 mt-3">
                        <label htmlFor='name' className='form-label'>
                            Name
                        </label>
                        <input type='text' className='form-control' id='name' name='name' onChange={handleInputChange} value={formData.name}/>
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='birthdate' className='form-label'>
                            Birthdate
                        </label>
                        <input type='text' className='form-control' id='birthdate' name='birthdate' onChange={handleInputChange} value={formData.birthdate}/>
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='gender' className='form-label'>
                            Gender
                        </label>
                        <input type='text' className='form-control' id='gender' name='gender' onChange={handleInputChange} value={formData.gender}/>
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='nationality' className='form-label'>
                            Nationality
                        </label>
                        <input type='text' className='form-control' id='nationality' name='nationality' onChange={handleInputChange} value={formData.nationality}/>
                    </div>

                    <button type='submit' className='btn btn-primary'>
                        Submit
                    </button>

                </form>

                <table className='table  table-bordered table-striped table-hover'>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Birthdate</th>
                            <th>Gender</th>
                            <th>Nationality</th>
                            <th>Created at</th>
                            <th>Updated at</th>
                        </tr>
                    </thead>
                    <tbody>
                        {people.map((person) => (
                            <tr key={person.id}>
                                <td>{person.id}</td>
                                <td>{person.name}</td>
                                <td>{person.birthdate}</td>
                                <td>{person.gender}</td>
                                <td>{person.nationality}</td>
                                <td>{person.created_at}</td>
                                <td>{person.updated_at}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>

            </div>

        </div>
    )
}

export default App;