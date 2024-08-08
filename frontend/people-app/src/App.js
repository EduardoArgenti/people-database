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
                        Base de dados
                    </a>
                </div>
            </nav>

            <div className='container'>
                <h3>Formulário</h3>
                <form onSubmit={handleFormSubmit}>

                    <div className="mb-3 mt-3">
                        <label htmlFor='name' className='form-label'>
                            Nome
                        </label>
                        <input type='text' className='form-control' id='name' name='name' onChange={handleInputChange} value={formData.name}/>
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='birthdate' className='form-label'>
                            Data de nascimento
                        </label>
                        <input type='text' className='form-control' id='birthdate' name='birthdate' onChange={handleInputChange} value={formData.birthdate}/>
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='gender' className='form-label'>
                            Gênero
                        </label>
                        <input type='text' className='form-control' id='gender' name='gender' onChange={handleInputChange} value={formData.gender}/>
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='nationality' className='form-label'>
                            Nacionalidade
                        </label>
                        <input type='text' className='form-control' id='nationality' name='nationality' onChange={handleInputChange} value={formData.nationality}/>
                    </div>

                    <button type='submit' className='btn btn-primary'>
                        Salvar
                    </button>

                </form>
            </div>

            <div className='container'>
                <h3>Upload de CSV</h3>
                <form onSubmit={handleFormSubmit}>

                    <button type='submit' className='btn btn-primary'>
                        Carregar
                    </button>

                </form>
            </div>

            <div className='container'>
                <h3>Dados</h3>
                <table className='table  table-bordered table-striped table-hover'>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Data de nascimento</th>
                            <th>Gênero</th>
                            <th>Nacionalidade</th>
                            <th>Criado em</th>
                            <th>Atualizado em</th>
                            <th>Editar</th>
                            <th>Remover</th>
                        </tr>
                    </thead>
                    <tbody>
                        {people.map((person) => (
                            <tr key={person.id} style={{ verticalAlign: "middle"}}>
                                <td className="align-middle-custom">{person.id}</td>
                                <td className="align-middle-custom">{person.name}</td>
                                <td className="align-middle-custom">{person.birthdate}</td>
                                <td className="align-middle-custom">{person.gender}</td>
                                <td className="align-middle-custom">{person.nationality}</td>
                                <td className="align-middle-custom">{person.created_at}</td>
                                <td className="align-middle-custom">{person.updated_at}</td>
                                <td className="text-center align-middle-custom">
                                    <button className="alert alert-info" style={{ marginBottom: '0px', padding: '5px 12px' }}>
                                        <i className="fas fa-edit"></i>
                                    </button>
                                </td>
                                <td className="text-center align-middle-custom">
                                    <button className="alert alert-danger" style={{ marginBottom: '0px', padding: '5px 12px' }}>
                                        <i className="fas fa-trash-can"></i>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

        </div>
    )
}

export default App;