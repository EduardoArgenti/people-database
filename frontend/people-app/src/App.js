import React, { useState, useEffect } from 'react';
import api from './api';

const App = () => {
    const [people, setPeople] = useState([]);
    const [formData, setFormData] = useState({
        id: '',
        name: '',
        birthdate: '',
        gender: '',
        nationality: ''
    });
    const [file, setFile] = useState([]);
    const [editId, setEditId] = useState(null);
    const [filterColumn, setFilterColumn] = useState('');
    const [filterValue, setFilterValue] = useState('');
    const [keyword, setKeyword] = useState('');
    const [filteredIds, setFilteredIds] = useState([]);

    // Get records
    const fetchPeople = async () => {
        const response = await api.get('/people/', {
            params: {
                filter_column: filterColumn,
                filter_value: filterValue,
                keyword: keyword
            }
        });
        setPeople(response.data);
        setFilteredIds(response.data.map(person => person.id));
    };

    useEffect(() => {
        fetchPeople();
    }, [filterColumn, filterValue, keyword]);

    const handleFilterColumnChange = (event) => {
        setFilterColumn(event.target.value);
    };

    const handleFilterValueChange = (event) => {
        setFilterValue(event.target.value);
    };

    const handleKeywordChange = (event) => {
        setKeyword(event.target.value);
    }

    const fileDownload = async () => {
        console.log('ids', filteredIds);
        await api.post('/people/download', filteredIds)
            .then(response => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'filtered_people.csv');
                document.body.appendChild(link);
                link.click();
                link.remove();
            });
    };

    // Add or update records
    const handleFormSubmit = async (event) => {
        event.preventDefault();
        if (editId) {
            await api.put(`/people/${editId}`, formData);
            setEditId(null);
        } else {
            await api.post('/people/', formData);
        }
        fetchPeople();
        setFormData({
            name: '',
            birthdate: '',
            gender: '',
            nationality: ''
        });
    };

    const handleInputChange = (event) => {
        const value = event.target.value;
        setFormData({
            ...formData,
            [event.target.name]: value
        });
    };

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const fileUpload = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("file", file, file.name);
        await api.post(`/people/upload`, formData);
        fetchPeople();
        setFormData({
            name: '',
            birthdate: '',
            gender: '',
            nationality: ''
        });
    };

    // Delete record
    const deletePerson = async (id) => {
        await api.delete(`/people/${id}`);
        fetchPeople();
        setFormData({
            name: '',
            birthdate: '',
            gender: '',
            nationality: ''
        });
    }

    // Edit record
    const handleEdit = (person) => {
        setFormData({
            id: person.id,
            name: person.name,
            birthdate: person.birthdate,
            gender: person.gender,
            nationality: person.nationality
        });
        setEditId(person.id);
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
                        <input type='text' className='form-control' id='name' name='name' onChange={handleInputChange} value={formData.name} />
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='birthdate' className='form-label'>
                            Data de nascimento
                        </label>
                        <input type='text' className='form-control' id='birthdate' name='birthdate' onChange={handleInputChange} value={formData.birthdate} />
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='gender' className='form-label'>
                            Gênero
                        </label>
                        <input type='text' className='form-control' id='gender' name='gender' onChange={handleInputChange} value={formData.gender} />
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='nationality' className='form-label'>
                            Nacionalidade
                        </label>
                        <input type='text' className='form-control' id='nationality' name='nationality' onChange={handleInputChange} value={formData.nationality} />
                    </div>

                    <button type='submit' className='btn btn-primary'>
                        {editId ? 'Atualizar' : 'Salvar'}
                    </button>

                </form>
            </div>

            <div className='container'>
                <h3>Upload de CSV</h3>
                <form onSubmit={fileUpload}>
                    <input type="file" onChange={handleFileChange} />
                    <button type='submit' className='btn btn-primary'>
                        Salvar
                    </button>
                </form>
            </div>

            <div className='container'>
                <h3>Filtro</h3>
                <form>
                    <div className='mb-3'>
                        <label htmlFor='filterColumn' className='form-label'>
                            Coluna
                        </label>
                        <select
                            id='filterColumn'
                            className='form-select'
                            value={filterColumn}
                            onChange={handleFilterColumnChange}
                        >
                            <option value=''>Escolha uma coluna</option>
                            <option value='id'>ID</option>
                            <option value='name'>Nome</option>
                            <option value='gender'>Gênero</option>
                            <option value='nationality'>Nacionalidade</option>
                        </select>
                    </div>
                    <div className='mb-3'>
                        <label htmlFor='filterValue' className='form-label'>
                            Valor
                        </label>
                        <input
                            type='text'
                            id='filterValue'
                            className='form-control'
                            value={filterValue}
                            onChange={handleFilterValueChange}
                        />
                    </div>

                    <div className='mb-3'>
                        <label htmlFor='keyword' className='form-label'>
                            Palavra-chave
                        </label>
                        <input type='text' className='form-control' id='keyword' value={keyword} onChange={handleKeywordChange}/>
                    </div>
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
                            <tr key={person.id} style={{ verticalAlign: "middle" }}>
                                <td className="align-middle-custom">{person.id}</td>
                                <td className="align-middle-custom">{person.name}</td>
                                <td className="align-middle-custom">{person.birthdate}</td>
                                <td className="align-middle-custom">{person.gender}</td>
                                <td className="align-middle-custom">{person.nationality}</td>
                                <td className="align-middle-custom">{person.created_at}</td>
                                <td className="align-middle-custom">{person.updated_at}</td>
                                <td className="text-center align-middle-custom">
                                    <button
                                        onClick={() => handleEdit(person)} className="alert alert-info" style={{ marginBottom: '0px', padding: '5px 12px' }}>
                                        <i className="fas fa-edit"></i>
                                    </button>
                                </td>
                                <td className="text-center align-middle-custom">
                                    <button
                                        onClick={() => deletePerson(person.id)} className="alert alert-danger" style={{ marginBottom: '0px', padding: '5px 12px' }}>
                                        <i className="fas fa-trash-can"></i>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <button onClick={fileDownload} className='btn btn-success'>
                    Baixar CSV
                </button>
            </div>

        </div>
    )
}

export default App;