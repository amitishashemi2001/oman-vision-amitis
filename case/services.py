import sys
from .models import CaseLog, CaseSubStep
# SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def case_log_submit(not_updated_instance, request):
    try:
        updated_instance = CaseLog.objects.get(pk=not_updated_instance.pk)
        previous_substep = CaseSubStep.objects.filter(next=not_updated_instance.substep).first()
        current_substep = not_updated_instance.substep
        if current_substep.is_start:
            previous_substep = current_substep
        if current_substep.next is None:
            updated_instance.substep_status = 'DONE'
            updated_instance.case.case_status = 'FINISHED'
            updated_instance.save()
            updated_instance.case.save()
            return

        if bool(int(request.data.get('has_error'))):
            updated_instance.substep_status = 'FAILED'
            updated_instance.save()
            CaseLog.objects.create(
                case=updated_instance.case,
                substep=previous_substep
            )
            # send notification
        else:
            updated_instance.substep_status = 'DONE'
            updated_instance.save()
            CaseLog.objects.create(
                case=updated_instance.case,
                substep=updated_instance.substep.next
            )
            # send notification
    except Exception as e:
        print(f'Error in case log submit service : {e}', file=sys.stderr)
        raise e
