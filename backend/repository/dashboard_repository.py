"""
Dashboard Repository
Handles all database access.
"""

from sqlalchemy import text


class DashboardRepository:

    def __init__(self, engine):

        self.engine = engine


    # ==========================================================
    # PATIENT
    # ==========================================================

    def get_patient(self, patient_id):

        with self.engine.connect() as conn:

            result = conn.execute(

                text("""
                    SELECT *
                    FROM patients
                    WHERE patient_id=:id
                """),

                {"id": patient_id}

            )

            row = result.fetchone()

            return dict(row._mapping) if row else None


    # ==========================================================
    # PATIENT VITALS
    # ==========================================================

    def get_patient_vitals(self, patient_id):

        with self.engine.connect() as conn:

            result = conn.execute(

                text("""
                    SELECT *
                    FROM vital_features
                    WHERE patient=:id
                    ORDER BY date
                """),

                {"id": patient_id}

            )

            return [

                dict(row._mapping)

                for row in result

            ]


    # ==========================================================
    # REFERENCE RANGE
    # ==========================================================

    def get_reference(self, age_band):

        with self.engine.connect() as conn:

            result = conn.execute(

                text("""
                    SELECT *
                    FROM reference_ranges
                    WHERE age_band=:band
                """),

                {"band": age_band}

            )

            row = result.fetchone()

            return dict(row._mapping) if row else None


    # ==========================================================
    # PATIENT LIST
    # ==========================================================

    def get_all_patients(self):

        with self.engine.connect() as conn:

            result = conn.execute(

                text("""
                    SELECT *
                    FROM patients
                    ORDER BY patient_id
                """)

            )

            return [

                dict(row._mapping)

                for row in result

            ]
        # ==========================================================
    # PATIENT WITH GLUCOSE
    # ==========================================================

    def get_patient_with_glucose(self):

        with self.engine.connect() as conn:

            result = conn.execute(

                text("""
                    SELECT DISTINCT patient
                    FROM vital_features
                    WHERE description LIKE '%Glucose%'
                    LIMIT 1
                """)

            )

            row = result.fetchone()

            return row[0] if row else None
    
        # ==========================================================
    # COMPLETE DASHBOARD PATIENT
    # ==========================================================

    def get_patient_with_complete_dashboard(self):

        with self.engine.connect() as conn:

            result = conn.execute(

                text("""
                    SELECT patient

                    FROM vital_features

                    GROUP BY patient

                    HAVING
                        COUNT(
                            DISTINCT description
                        ) >= 3

                    LIMIT 1
                """)

            )

            row = result.fetchone()

            return row[0] if row else None