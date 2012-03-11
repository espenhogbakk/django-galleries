$(function(){

    var min_width = parseInt($("#gallery").data('aspect-ratio').split("/")[0])
    var min_height = parseInt($("#gallery").data('aspect-ratio').split("/")[1])
    MIN_SIZE = [min_width, min_height]
    ASPECT_RATIO = min_width/min_height
    
    var gallery_select = $("#id_gallery")
    $(gallery_select).bind("change", function(e) {
        // Switcing galleries
        var id = $(gallery_select).val()
        if (id != '') {
            Images.url = '/admin/galleries/galleries/' + $(gallery_select).val() + '/images'
            window.Gallery = new GalleryView
        }
    })
    
    GALLERY_ID = gallery_select.val()
    
    window.Gallery = Backbone.Model.extend()
    
    window.GalleryImage = Backbone.Model.extend()

    window.GalleryImages = Backbone.Collection.extend({
        model: GalleryImage,
        url: '/admin/galleries/galleries/' + GALLERY_ID + '/images',

        parse: function(response) {
            return response.images
        }
        
    })
    
    // Initiate the GalleryImages collection
    window.Images = new GalleryImages;
    
    window.ImageView = Backbone.View.extend({
        
        tagName: "li",
        
        template: _.template('<li class="image"><a href="<%= croppable %>"><img data-id="<%= id %>" data-org-width="<%= org_width %>" data-org-height="<%= org_height %>" src="<%= thumbnail %>"></a></li>'),
        
        initialize: function() {
            this.model.bind('change', this.render, this);
            this.model.bind('destroy', this.remove, this);
        },
        
        render: function() {
            var model = this.model
            
            var html = this.template(this.model.toJSON())
            $(this.el).html(html)
            
            // Add jcrop to every image
            // Add fancybox to images
            function formatTitle(title, currentArray, currentIndex, currentOpts) {
                var saveBtn = '<div id="fancybox-title" class="fancybox-title-float" style="left: 217px; display: block; "><table id="fancybox-title-float-wrap" cellpadding="0" cellspacing="0"><tbody><tr><td id="fancybox-title-float-left"></td><td id="fancybox-title-float-main"><a style="color: #fff" href="javascript:;" onclick="saveCropping();">Save</a></td><td id="fancybox-title-float-right"></td></tr></tbody></table></div>'
                var cancelBtn = '<div id="fancybox-title" class="fancybox-title-float" style="left: 277px; display: block; "><table id="fancybox-title-float-wrap" cellpadding="0" cellspacing="0"><tbody><tr><td id="fancybox-title-float-left"></td><td id="fancybox-title-float-main"><a style="color: #fff" href="javascript:;" onclick="$.fancybox.close();">Cancel</a></td><td id="fancybox-title-float-right"></td></tr></tbody></table></div>'
                return saveBtn + cancelBtn
            }
            
            $("a", this.el).fancybox({
                showCloseButton: false,
                titlePosition: 'outside',
                titleFormat: formatTitle,
                onComplete: fancyBoxCropper,
                //onCleanup: fancyBoxCropperCloses
            })

            coordinates = new Object
            id = undefined
            
            function fancyBoxCropper(e) {
                var org_width = $("img", e).data('org-width')
                var org_height = $("img", e).data('org-height')
                id = $("img", e).data('id')
                image = Images.get(id)
                
                var options = {
                    aspectRatio: ASPECT_RATIO,
                    minSize: MIN_SIZE,
                    trueSize: [org_width, org_height],
                    allowMove: true,
                    onSelect: handleSelect,
                }
                
                // If there are cropping, set initial crop
                var cropping = image.get("cropping")
                if (cropping != '') {
                    var s = cropping.split(',');
                    var initial = [
                        parseInt(s[0], 10),
                        parseInt(s[1], 10),
                        parseInt(s[2], 10),
                        parseInt(s[3], 10)
                    ]
                    $.extend(options, {setSelect: initial});
                }
                

                $("#fancybox-img").Jcrop(options)

                function handleSelect(c) {
                    coordinates.x = c.x
                    coordinates.y = c.y
                    coordinates.x2 = c.x2
                    coordinates.y2 = c.y2
                }
            }

    
            window.saveCropping = function() {
              $.fancybox.close()
              saveCroppingValue()
            }
        
            function saveCroppingValue() {
                // Save the coordinates on the GalleryImage
                // First make it into a commaseperated list
                var cropping = []
                for (var i in coordinates) {
                    cropping.push(coordinates[i])
                }
                cropping = cropping.toString()
                
                // Find the GalleryImage
                // Should be able to do "this.model", but for some reason
                // this models always refer to the last initiated one.
                image = Images.get(id)
                image.set({
                    cropping: cropping
                })
                // Update cropping value on image
                image.save({}, {
                    silent: true,
                    success: function (model, response) {
                        model.set({thumbnail: response.image.thumbnail}, {silent: true})
                        model.change()
                    }
                })
            }
            
            
            // Add delete option on hover
            $(this.el).mouseenter(function() {
              $(this).append(
                $('<a />', {
                  'text': 'Slett',
                  'class': 'deleteBtn'
                }).click(function(e) {
                  console.log("DELETE IMAGE")
                  model.destroy()
                })
              )
            })
            $(this.el).mouseleave(function() {
              $('.deleteBtn', this).remove()
            })



            return this
        },
        
        remove: function() {
            $(this.el).remove()
        },
        
        clear: function() {
            this.model.destroy()
        }
        
    })
    
    window.GalleryView = Backbone.View.extend({

        el: "#gallery",
        
        events: {
            "change input[type=file]": "upload",
        },
        
        initialize: function() {
            Images.bind('add', this.addOne, this)
            Images.bind('reset', this.addAll, this)
            Images.fetch()
            
            // Make list sortable
            $("ul", this.el).sortable({
                update: function(event, ui) {
                    // Get the image that has moved
                    //var id = $("img", ui.item).data('id')
                    //var image = Images.get(id)
                    
                    // Loop through all images, and update their order attribute
                    var images = $(this).find("img")
                    images.each(function(i) {
                        var image = Images.get($(this).data("id"))
                        image.set({ order: i+1 })
                        image.save()
                    })
                    
                }
            })
            
            // Add drop event handler for uploadin
            $("#upload").dropArea().bind("drop", this.drop)

            // Rearrange position of the "add button"
            $("#add_id_gallery").prependTo($("#add_id_gallery").parent())
            $("#id_gallery").prependTo($("#id_gallery").parent())
        },
        
        addOne: function(image) {
            var view = new ImageView({model: image})
            $("ul", "#gallery").append(view.render().el)
        },
        
        addAll: function() {
            // Clear images already present
            $("ul", "#gallery").html('')
            Images.each(this.addOne);
        },
        
        drop: function(e) {
            e.stopPropagation()
            e.preventDefault()
            e = e.originalEvent
            
            files = e.dataTransfer.files
            for (var i in files) {
                if ( typeof files[i] == "object" ) {
                    var file = files[i]
                    uploadDrop(file)
                }
            }
            
            function uploadDrop(file) {
                $.upload("/admin/galleries/galleries/" + GALLERY_ID + "/images/", {
                    image: file, gallery: GALLERY_ID
                }, function(data) {
                    var image = new GalleryImage(data.image) 
                    Images.add(image)
                })
            }
        },
    
        upload: function(e) {
            var target = e.currentTarget
            _.each(target.files, function(file) {

                $.upload("/admin/galleries/galleries/" + GALLERY_ID + "/images/", {
                    image: file, gallery: GALLERY_ID
                }, function(data) {
                    var image = new GalleryImage(data.image) 
                    Images.add(image)
                })
            })

            e.stopPropagation()
            e.preventDefault()
            return false
        },
        
    })
    
    window.Gallery = new GalleryView
})