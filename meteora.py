from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import _get_queryset
from django.utils.translation import ugettext_lazy as _
# Compatible with meteora 0.6
from utils import json

class Meteora:
    """
        Meteora Class

        @success(bool) for send errorMessage as False and successMessage with True
        @message(str) the message sended.
        if @success @message not passed on meteora object not add the message: error or success

        m = Meteora(True,"Message Success" )
        return m.json_response()

        m = Meteora()
        ...
        dosomething()
        ....
        return m.json_response()
    """
    def __init__(self, success = None, message = None ):
        self.message = {}
        self.execute_js= []

        if success is None and message is None:
            return

        if success is False:
            self.message["errorMessage"]= message
            if self.message.has_key("successMessage"):
                del self.message["successMessage"]
        else:
            self.message["successMessage"]= message
            if self.message.has_key("errorMessage"):
                del self.message["errorMessage"]


    def bubble(self, id, message ):
        """
            Show a bubbly across json respose
            @id(str) input where bubble will show
            @message(str) message


            m = Meteora()
            m.bubble("id_field","Bar!")
            return m.json_response()


            http://meteora.astrata.com.mx/pages/documentation/control-bubble
        """
        self.execute(" var b = new Bubble('%s','%s'); b.show(); " % ( id, message) )

    def json_response(self):
        """
            json response from Meteora Object.
            it always will return for json encode.
        """
        return json(self.message)

    def more_execute(self, execute):
        """
            add More execute comandas

            m = Meteora()
            m.bubble("blah","foo")
            m.more_execute(" dosomething() ")
            return m.json_response()
        """
        self.execute_js.append(execute)

    def execute(self, execute = False ):
        """
            execute a commands

            m = Meteora()
            m.execute(" alert('hi'); ")
            return m.json_response()
        """
        if execute:
            self.execute_js.append(execute)
        if "execute" in self.message:
            self.message["execute"] += "".join(self.execute_js).replace("\n",'')
        else:
            self.message["execute"] = "".join(self.execute_js).replace("\n",'')
        self.execute_js = []

    def form_invalid(self,form ):
        """
        """
        if not form.is_valid():
            for id,errors in form.errors.items():
                for error in errors:
                    self.bubble("id_" + id,error.decode("UTF"))
        #self.execute("$('%s').innerHTML='<table>%s</table>';" % ( table_id, form.as_table() ) )

    #Notebooks def
    def notebook_close_page(self, notebook, id ):
        """
            Close a page from a notebook
            @notebook(str) id of notebook
            @id page ID for close

            m = Meteora(True, "Page Closed")
            m.notebook_close_page("myNotebook",'page1')
            return m.json_response()

            http://meteora.astrata.com.mx/pages/documentation/control-notebook
        """
        self.execute_js.append(" var nb = document.%s; nb.closePage('%s');" % ( notebook, id ) )
        self.execute()
    def notebook_select_page(self, notebook, id ):
        """
            Select a page from a notebook

            @notebook(str) id of notebook
            @id page ID for close

            m = Meteora(True, "Page Closed")
            m.notebook_select_page("myNotebook",'page1')
            return m.json_response()

            http://meteora.astrata.com.mx/pages/documentation/control-notebook
        """
        self.execute_js.append(" var nb = document.%s; nb.selectPage('%s');" % (notebook,id) )
        self.execute()

    # jsonRpc Core  defs
    # http://meteora.astrata.com.mx/pages/documentation/core-jsonrpc
    def redirectTo(self, url ):
        """
            @url(str) format: "/blah/url"  or "http://google.com" or app view

            m = Meteora()
            m.redirectTo("/foo/bar")
            return m.json_response()

        """
        self.message["redirectTo"] = url
        return self

    def update_object(self, object_id, view):
        self.message['updateObject'] = {'objectId': object_id, 'data' : view}

    def update_object_url(self, object_id, url ):
        self.message['updateObject'] = {'objectId': object_id, 'dataSource' : url}

    def delete_object(self, object_id):
        self.message['deleteObject'] = object_id

    def error_message(self, string):
        self.message['errorMessage'] = string

    def hide_object(self, object_id):
        self.message['hideObject'] = object_id

    def show_object(self, object_id):
        self.message['showObject'] = object_id

class MeteoraError(Exception):
    pass


