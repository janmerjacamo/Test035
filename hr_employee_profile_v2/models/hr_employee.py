from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # -------------------------------------------------------------------------
    # Campos heredados de versiones previas del módulo.
    # Se conservan para no perder datos al actualizar el módulo en una BD donde
    # ya estaba instalado, aunque la nueva vista usa nombres más ordenados.
    # -------------------------------------------------------------------------
    x_department_work = fields.Char("Departamento Trabajo")
    x_service_position = fields.Char("Puesto de Servicio")
    x_hr_responsible = fields.Char("Responsable RRHH")
    x_birth_place_custom = fields.Char("Lugar de Nacimiento")
    x_emergency_phone_custom = fields.Char("Teléfono Emergencia")
    x_children_qty = fields.Integer("Número Hijos")
    x_siblings_qty = fields.Integer("Número Hermanos")
    x_direct_manager_custom = fields.Char("Jefe Inmediato")
    x_new_position = fields.Char("Nuevo Puesto")

    # -------------------------------------------------------------------------
    # Datos personales complementarios Guatemala / RRHH operativo
    # -------------------------------------------------------------------------
    x_home_phone = fields.Char("Teléfono de Casa")
    x_age = fields.Integer("Edad", compute="_compute_x_age", store=True)
    x_dpi = fields.Char("DPI")
    x_dpi_extended = fields.Char("DPI Extendido en")
    x_nit = fields.Char("NIT")
    x_driver_license = fields.Char("Licencia de Conducir")
    x_igss = fields.Char("Afiliación IGSS")
    x_municipality = fields.Char("Municipio de Residencia")
    x_department_residence = fields.Char("Departamento de Residencia")
    x_housing_type = fields.Selection([
        ("propio", "Propio"),
        ("alquilado", "Alquilado"),
        ("familiar", "Familiar"),
    ], string="Tipo de Vivienda")
    x_years_residence = fields.Char("Tiempo de Vivir Allí")
    x_other_income = fields.Boolean("Posee Otros Ingresos")
    x_other_income_notes = fields.Char("Detalle de Otros Ingresos")
    x_has_vehicle = fields.Boolean("Posee Vehículo")
    x_vehicle_type = fields.Char("Tipo de Vehículo")
    x_vehicle_brand = fields.Char("Marca de Vehículo")
    x_has_debts = fields.Boolean("Posee Deudas")
    x_debt_amount = fields.Float("Monto de Deuda")
    x_addresses_notes = fields.Text("Direcciones / Referencias de Ubicación")

    # -------------------------------------------------------------------------
    # Datos familiares complementarios
    # -------------------------------------------------------------------------
    x_father_name = fields.Char("Nombre del Padre")
    x_father_phone = fields.Char("Teléfono del Padre")
    x_mother_name = fields.Char("Nombre de la Madre")
    x_mother_phone = fields.Char("Teléfono de la Madre")
    x_spouse_name = fields.Char("Nombre del Cónyuge")
    x_spouse_phone = fields.Char("Teléfono del Cónyuge")
    x_spouse_address = fields.Char("Dirección del Cónyuge")
    x_children_count = fields.Integer("Número de Hijos")
    x_siblings_count = fields.Integer("Número de Hermanos")

    # -------------------------------------------------------------------------
    # Salud
    # -------------------------------------------------------------------------
    x_smokes = fields.Boolean("Fuma")
    x_drinks = fields.Boolean("Bebe")
    x_sports = fields.Boolean("Realiza Actividades Deportivas")
    x_weight = fields.Float("Peso")
    x_height = fields.Float("Altura")
    x_disabilities = fields.Text("Impedimentos")
    x_disease = fields.Text("Padece Alguna Enfermedad")
    x_medication = fields.Text("Toma Algún Medicamento")
    x_blood_type = fields.Selection([
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ], string="Tipo de Sangre")

    # -------------------------------------------------------------------------
    # Trabajo complementario
    # -------------------------------------------------------------------------
    x_job_position_service = fields.Char("Nombre del Puesto de Servicio")
    x_reentry_date = fields.Date("Fecha de Reingreso")
    x_job_address = fields.Char("Dirección del Puesto")
    x_direct_manager = fields.Char("Jefe Inmediato")
    x_assigned_department = fields.Char("Departamento Asignado")
    x_position_change_date = fields.Date("Fecha de Cambio de Puesto")
    x_new_position_name = fields.Char("Nombre del Puesto Nuevo")
    x_contract_condition = fields.Selection([
        ("contrato", "Contrato"),
        ("fijo", "Fijo"),
        ("temporal", "Temporal"),
    ], string="Condición Laboral")
    x_benefits = fields.Selection([
        ("none", "Sin Prestaciones"),
        ("full", "Completas"),
        ("half", "50%"),
    ], string="Prestaciones")

    # -------------------------------------------------------------------------
    # Relaciones repetibles
    # -------------------------------------------------------------------------
    x_labor_experience_ids = fields.One2many(
        "hr.employee.labor.experience", "employee_id", string="Experiencia Laboral"
    )
    x_personal_reference_ids = fields.One2many(
        "hr.employee.personal.reference", "employee_id", string="Referencias Personales"
    )
    x_education_ids = fields.One2many(
        "hr.employee.education.record", "employee_id", string="Estudios"
    )
    x_technical_study_ids = fields.One2many(
        "hr.employee.technical.study", "employee_id", string="Estudios Técnicos"
    )

    # -------------------------------------------------------------------------
    # Documentos específicos solicitados
    # -------------------------------------------------------------------------
    x_vaccine_card = fields.Binary("Carné de Vacunas", attachment=True)
    x_vaccine_card_filename = fields.Char("Archivo Carné de Vacunas")
    x_lung_card = fields.Binary("Tarjeta de Pulmones", attachment=True)
    x_lung_card_filename = fields.Char("Archivo Tarjeta de Pulmones")
    x_fingerprints = fields.Binary("Huellas", attachment=True)
    x_fingerprints_filename = fields.Char("Archivo Huellas")
    x_document_acknowledgement = fields.Binary("Reconocimiento de Documentos", attachment=True)
    x_document_acknowledgement_filename = fields.Char("Archivo Reconocimiento")
    x_authorized_work_contract = fields.Binary("Contrato de Trabajo Autorizado", attachment=True)
    x_authorized_work_contract_filename = fields.Char("Archivo Contrato Autorizado")

    @api.depends("birthday")
    def _compute_x_age(self):
        today = fields.Date.context_today(self)
        for employee in self:
            employee.x_age = relativedelta(today, employee.birthday).years if employee.birthday else 0


class HrEmployeeLaborExperience(models.Model):
    _name = "hr.employee.labor.experience"
    _description = "Experiencia Laboral del Empleado"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True, ondelete="cascade")
    company_name = fields.Char("Nombre de Empresa")
    position = fields.Char("Puesto que Ocupaba")
    time_worked = fields.Char("Tiempo Laborado")
    salary = fields.Float("Salario")
    leaving_reason = fields.Char("Motivo de Retiro")
    immediate_boss = fields.Char("Jefe Inmediato")
    company_phone = fields.Char("Teléfono de la Empresa")
    can_request_reference = fields.Selection([
        ("yes", "Sí"),
        ("no", "No"),
    ], string="¿Se puede pedir referencias?")


class HrEmployeePersonalReference(models.Model):
    _name = "hr.employee.personal.reference"
    _description = "Referencia Personal del Empleado"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True, ondelete="cascade")
    name = fields.Char("Nombre")
    phone = fields.Char("Teléfono")
    relationship = fields.Char("Parentesco")


class HrEmployeeEducationRecord(models.Model):
    _name = "hr.employee.education.record"
    _description = "Estudio del Empleado"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True, ondelete="cascade")
    degree = fields.Char("Título Obtenido")
    year = fields.Char("Año")
    institution = fields.Char("Institución")
    currently_studying = fields.Boolean("Estudia Actualmente")
    schedule = fields.Char("Horario")


class HrEmployeeTechnicalStudy(models.Model):
    _name = "hr.employee.technical.study"
    _description = "Estudio Técnico del Empleado"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True, ondelete="cascade")
    technical_study = fields.Char("Estudio Técnico")
    degree = fields.Char("Título Obtenido")
    year = fields.Char("Año")
    institution = fields.Char("Institución")
