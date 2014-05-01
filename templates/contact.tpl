<div class="row">
    <h2>{{ target }} a Contact</h2>
    %if defined('error'):
    <h1>{{ error }}</h1>
    %end
    <form role="form" action="{{ action }}" method="POST"
    enctype="multipart/form-data">

    %# Render all fields in the variable passed to template as 'form'
    %for field in form:

    %# The next line of code is a bit weird.  According to the Bottle
    %# docs, the way to check whether a variable is defined in the
    %# current template namespace is to pass the variable ENCLOSED IN
    %# QUOTES to the 'defined()' function.

        %if defined('field'):
            %if field.id != "photo":
            %if field.errors:
                <div class="form-group has-error">
            %else:
                <div class="form-group">
            %end
                <div class="input-group">
                {{ !field.label() }}:
                %if field.errors:
                    %for error in field.errors:
                        {{ error }}
                    %end
                %end
                %if field.id == "state":
                    {{ !field(class_="form-control") }}
                %else:
                    {{ !field(class_="form-control", size="100", maxlength="100") }}
                %end
                </div>
            </div>
            %end
        %end
    %end
       <div class="form-group">
       {{ !form.photo.label() }}:
       {{ !form.photo() }}
       </div>
       <div class="btn-group btn-group-justified">
         <div class="btn-group">
           <button type="submit" class="btn btn-primary" value="save">Save Contact</button>
         </div>
         <div class="btn-group">
           <a href="/" class="btn btn-danger">Cancel</a>
         </div>
       </div>
   </form>
</div>
