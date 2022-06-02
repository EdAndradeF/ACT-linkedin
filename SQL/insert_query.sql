INSERT INTO atividade (id_atividade, atividade) VALUES 
	(4, 'Currículo baixado'),
	(3, 'Candidatura visualizada'),
    (2, 'Candidatura enviada'),
    (1, 'Candidatou-se no site da empresa')
	;

INSERT INTO nivel_cargo (id_nivel, nivel) VALUES
	(0, 'Nao-informado'),
	(1, 'Estágio'),
	(2, 'Assistente'),
	(3, 'Júnior'),
	(4, 'Pleno-sênior'),
	(5, 'Diretor'),
	(6, 'Executivo')
	;

INSERT INTO modelo_trabalho (id_modelo, modelo) VALUES 
	(1, 'Presencial'),
	(2, 'Remoto'),
	(3, 'Híbrido')
	(0, 'Nao-informado')
	;

INSERT INTO tipo_contratacao (id_tipo, tipo) VALUES 
	(1, 'Tempo integral'),
	(2, 'Meio período'),
	(3, 'Contrato'),
	(4, 'Temporário'),
	(5, 'Voluntário'),
	(6, 'Estágio'),
	(0, 'Outro')
	;

INSERT INTO quantidade_funcionario (id_quantidade, quantidade) VALUES 
 	(0, 'nao informado'),
 	(1, '1 ex-funcionários da empresa'),
 	(2, '1-10 funcionários'),
 	(3, '11-50 funcionários'),
 	(4, '51-200 funcionários'),
 	(5, '201-500 funcionários'),
 	(6, '501-1.000 funcionários'),
 	(7, '1.001-5.000 funcionários'),
 	(8, '5.001-10.000 funcionários'),
 	(9, '+ de 10.001 funcionários')
	;