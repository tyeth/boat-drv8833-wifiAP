var JoyStick = (function(container, parameters)
 {
     parameters = parameters || {};
     var title = (typeof parameters.title === "undefined" ? "joystick" : parameters.title),
         width = (typeof parameters.width === "undefined" ? 0 : parameters.width),
         height = (typeof parameters.height === "undefined" ? 0 : parameters.height),
         internalFillColor = (typeof parameters.internalFillColor === "undefined" ? "#00AA0011" : parameters.internalFillColor),
         internalLineWidth = (typeof parameters.internalLineWidth === "undefined" ? 2 : parameters.internalLineWidth),
         internalStrokeColor = (typeof parameters.internalStrokeColor === "undefined" ? "#00330077" : parameters.internalStrokeColor),
         externalLineWidth = (typeof parameters.externalLineWidth === "undefined" ? 2 : parameters.externalLineWidth),
         externalStrokeColor = (typeof parameters.externalStrokeColor ===  "undefined" ? "#008000" : parameters.externalStrokeColor),
         autoReturnToCenter = (typeof parameters.autoReturnToCenter === "undefined" ? true : parameters.autoReturnToCenter);
     
     // Create Canvas element and add it in the Container object
     var objContainer = document.getElementById(container);
     var canvas = document.createElement("canvas");
     canvas.id = title;
     if(width === 0) { width = objContainer.clientWidth; }
     if(height === 0) { height = objContainer.clientHeight; }
     canvas.width = width;
     canvas.height = height;
     objContainer.appendChild(canvas);
     var context=canvas.getContext("2d");
     
     var pressed = 0; // Bool - 1=Yes - 0=No
     var circumference = 2 * Math.PI;
     var smallestDimension = Math.min(canvas.width,canvas.height);
     var internalRadius = (smallestDimension-((smallestDimension/2)+10))/2;
     var maxMoveStick = internalRadius + 5;
     var externalRadius = internalRadius + 30;
     var centerX = canvas.width / 2;
     var centerY = canvas.height / 2;
     var directionHorizontalLimitPos = canvas.width / 10;
     var directionHorizontalLimitNeg = directionHorizontalLimitPos * -1;
     var directionVerticalLimitPos = canvas.height / 10;
     var directionVerticalLimitNeg = directionVerticalLimitPos * -1;
     // Used to save current position of stick
     var movedX=centerX;
     var movedY=centerY;
 
     touchSupport = function(){
         var hasTouchScreen = false;
         if ("maxTouchPoints" in navigator) {
             hasTouchScreen = navigator.maxTouchPoints > 0;
         } else if ("msMaxTouchPoints" in navigator) {
             hasTouchScreen = navigator.msMaxTouchPoints > 0;
         } else {
             var mQ = window.matchMedia && matchMedia("(pointer:coarse)");
             if (mQ && mQ.media === "(pointer:coarse)") {
                 hasTouchScreen = !!mQ.matches;
             } else if ('orientation' in window) {
                 hasTouchScreen = true; // deprecated, but good fallback
             } else {
                 // Only as a last resort, fall back to user agent sniffing
                 var UA = navigator.userAgent;
                 hasTouchScreen = (
                     /\b(BlackBerry|webOS|iPhone|IEMobile)\b/i.test(UA) ||
                     /\b(Android|Windows Phone|iPad|iPod)\b/i.test(UA)
                 );
             }
         }
         return hasTouchScreen;
     };
     
     // Check if the device support the touch or not
     if(touchSupport())
     {
         canvas.addEventListener("touchstart", onTouchStart, false);
         canvas.addEventListener("touchmove", onTouchMove, false);
         canvas.addEventListener("touchend", onTouchEnd, false);
     }
     //else
     {
         canvas.addEventListener("mousedown", onMouseDown, false);
         canvas.addEventListener("mousemove", onMouseMove, false);
         canvas.addEventListener("mouseup", onMouseUp, false);
     }
     // Draw the object
     drawExternal();
     drawInternal();
 
     function drawExternal()
     {
         context.beginPath();
         context.arc(centerX, centerY, externalRadius, 0, circumference, false);
         context.lineWidth = externalLineWidth;
         context.strokeStyle = externalStrokeColor;
         context.stroke();
     }
  
     function drawInternal()
     {
         context.beginPath();
         if(movedX<internalRadius) { movedX=maxMoveStick; }
         if((movedX+internalRadius) > canvas.width) { movedX = canvas.width-(maxMoveStick); }
         if(movedY<internalRadius) { movedY=maxMoveStick; }
         if((movedY+internalRadius) > canvas.height) { movedY = canvas.height-(maxMoveStick); }
         context.arc(movedX, movedY, internalRadius, 0, circumference, false);
         // create radial gradient
         var grd = context.createRadialGradient(centerX, centerY, 5, centerX, centerY, 200);
         // Light color
         grd.addColorStop(0, internalFillColor);
         // Dark color
         grd.addColorStop(1, internalStrokeColor);
         context.fillStyle = grd;
         context.fill();
         context.lineWidth = internalLineWidth;
         context.strokeStyle = internalStrokeColor;
         context.stroke();
     }
      
     function onTouchStart(event) 
     {
         pressed = 1;
     }
 
     function onTouchMove(event)
     {
         // Prevent the browser from doing its default thing (scroll, zoom)
         event.preventDefault();
         if(pressed === 1 && event.targetTouches[0].target === canvas)
         {
             movedX = event.targetTouches[0].pageX;
             movedY = event.targetTouches[0].pageY;
             // Manage offset
             if(canvas.offsetParent.tagName.toUpperCase() === "BODY")
             {
                 movedX -= canvas.offsetLeft;
                 movedY -= canvas.offsetTop;
             }
             else
             {
                 movedX -= canvas.offsetParent.offsetLeft;
                 movedY -= canvas.offsetParent.offsetTop;
             }
             // Delete canvas
             context.clearRect(0, 0, canvas.width, canvas.height);
             // Redraw object
             drawExternal();
             drawInternal();
         }
     }
 
     function onTouchEnd(event) 
     {
         pressed = 0;
         // If required reset position store variable
         if(autoReturnToCenter)
         {
             movedX = centerX;
             movedY = centerY;
         }
         // Delete canvas
         context.clearRect(0, 0, canvas.width, canvas.height);
         // Redraw object
         drawExternal();
         drawInternal();
         //canvas.unbind('touchmove');
     }
 
 
     function onMouseDown(event) 
     {
         pressed = 1;
     }
 
     function onMouseMove(event) 
     {
         if(pressed === 1)
         {
             movedX = event.pageX;
             movedY = event.pageY;
             // Manage offset
             if(canvas.offsetParent.tagName.toUpperCase() === "BODY")
             {
                 movedX -= canvas.offsetLeft;
                 movedY -= canvas.offsetTop;
             }
             else
             {
                 movedX -= canvas.offsetParent.offsetLeft;
                 movedY -= canvas.offsetParent.offsetTop;
             }
             // Delete canvas
             context.clearRect(0, 0, canvas.width, canvas.height);
             // Redraw object
             drawExternal();
             drawInternal();
         }
     }
 
     function onMouseUp(event) 
     {
         pressed = 0;
         // If required reset position store variable
         if(autoReturnToCenter)
         {
             movedX = centerX;
             movedY = centerY;
         }
         // Delete canvas
         context.clearRect(0, 0, canvas.width, canvas.height);
         // Redraw object
         drawExternal();
         drawInternal();
         //canvas.unbind('mousemove');
     }
 
 
     this.GetWidth = function () 
     {
         return canvas.width;
     };
      
     this.GetHeight = function () 
     {
         return canvas.height;
     };
      
     this.GetPosX = function ()
     {
         return movedX;
     };
     
     
     this.GetPosY = function ()
     {
         return movedY;
     };
     
    
     this.GetX = function ()
     {
         return Math.max(-100,Math.min(100, (100*((movedX - centerX)/maxMoveStick)))).toFixed();
     };
 
     
     this.GetY = function ()
     {
         return Math.max(-100,Math.min(100, ((100*((movedY - centerY)/maxMoveStick))*-1))).toFixed();
     };
      
     this.GetDir = function()
     {
         var result = "";
         var orizontal = movedX - centerX;
         var vertical = movedY - centerY;
         
         if(vertical >= directionVerticalLimitNeg && vertical <= directionVerticalLimitPos)
         {
             result = "C";
         }
         if(vertical < directionVerticalLimitNeg)
         {
             result = "N";
         }
         if(vertical > directionVerticalLimitPos)
         {
             result = "S";
         }
         
         if(orizontal < directionHorizontalLimitNeg)
         {
             if(result === "C")
             { 
                 result = "W";
             }
             else
             {
                 result += "W";
             }
         }
         if(orizontal > directionHorizontalLimitPos)
         {
             if(result === "C")
             { 
                 result = "E";
             }
             else
             {
                 result += "E";
             }
         }
         
         return result;
     };
 });
 