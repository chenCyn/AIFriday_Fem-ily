class BaseUser:
    def __init__(self, user_id, name, age, location, role):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.location = location
        self.role = role

    def to_profile_text(self):
        return f"{self.role.capitalize()} {self.name}, Age {self.age}, Location: {self.location}"

    def to_metadata(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "age": self.age,
            "location": self.location,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data):
        # Normalize role safely
        role_val = data.get("role")
        role = role_val.lower() if isinstance(role_val, str) else ""

        if role == "patient":
            return Patient.from_dict(data)
        # elif role == "volunteer":
        #     return Volunteer.from_dict(data)
        else:
            return cls(
                user_id=data.get("id"),
                name=data.get("name"),
                age=data.get("age"),
                location=data.get("location"),
                role=role,
            )
            
            
class Patient(BaseUser):
    def __init__(self, user_id, name, age, location, education, income_level,
                 employment, insurance_coverage, appointment_access,
                 admission_stats, notes, lpd, risk_factor, due_date,
                 actual_delivery_date, outcome):
        super().__init__(user_id, name, age, location, "patient")
        self.education = education
        self.income_level = income_level
        self.employment = employment
        self.insurance_coverage = insurance_coverage
        self.appointment_access = appointment_access
        self.admission_stats = admission_stats
        self.notes = notes
        self.lpd = lpd
        self.risk_factor = risk_factor
        self.due_date = due_date
        self.actual_delivery_date = actual_delivery_date
        self.outcome = outcome

    def to_profile_text(self):
        return (
            f"Patient {self.name}, Age {self.age}, Location: {self.location}, "
            f"Education: {self.education}, Employment: {self.employment}, "
            f"Risk: {self.risk_factor}, Due Date: {self.due_date}, Outcome: {self.outcome}"
        )

    def to_metadata(self):
        meta = super().to_metadata()
        meta.update({
            "education": self.education,
            "income_level": self.income_level,
            "employment": self.employment,
            "insurance_coverage": self.insurance_coverage,
            "appointment_access": self.appointment_access,
            "admission_stats": self.admission_stats,
            "notes": self.notes,
            "lpd": self.lpd,
            "risk_factor": self.risk_factor,
            "due_date": self.due_date,
            "actual_delivery_date": self.actual_delivery_date,
            "outcome": self.outcome,
        })
        return meta

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get("id"),
            name=data.get("Patient Name") or data.get("name"),
            age=data.get("Age"),
            location=data.get("Location"),
            education=data.get("Education"),
            income_level=data.get("Income Level"),
            employment=data.get("Employment"),
            insurance_coverage=data.get("Insurance Coverage"),
            appointment_access=data.get("Appointment Access"),
            admission_stats=data.get("Admission Stats"),
            notes=data.get("Notes"),
            lpd=data.get("LPD"),
            risk_factor=data.get("Risk Factor"),
            due_date=data.get("Due Date"),
            actual_delivery_date=data.get("Actual Delivery Date"),
            outcome=data.get("Outcome"),
        )


# class Volunteer(BaseUser):
#     def __init__(self, user_id, name, age, location, expertise):
#         super().__init__(user_id, name, age, location, "volunteer")
#         self.expertise = expertise
#
#     def to_profile_text(self):
#         return f"Volunteer {self.name}, Age {self.age}, Location: {self.location}, Expertise: {self.expertise}"
#
#     def to_metadata(self):
#         meta = super().to_metadata()
#         meta.update({
#             "expertise": self.expertise,
#         })
#         return meta
#
#     @classmethod
#     def from_dict(cls, data):
#         return cls(
#             user_id=data.get("id"),   
#             name=data.get("name"),
#             age=data.get("age"),
#             location=data.get("location"),
#             expertise=data.get("expertise"), 
#         )
